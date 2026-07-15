import uuid
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple

from fastapi_pagination import Params

from app.core.exceptions import AppException
from app.models import ChatSession, Message, MessageRole
from app.repositories import ChatRepository, MessageRepository
from app.services import OllamaService


class ChatService:
    """Business logic orchestrator for chat functionality."""

    def __init__(
        self,
        chat_repository: ChatRepository,
        message_repository: MessageRepository,
        ollama_service: OllamaService,
    ):
        self.chat_repository = chat_repository
        self.message_repository = message_repository
        self.ollama_service = ollama_service

    async def create_session(
        self, title: str, model: str, user_id: str = "default"
    ) -> ChatSession:
        """
        Create a new chat session.

        Args:
            title: Session title
            model: Model name to use
            user_id: User identifier

        Returns:
            Created ChatSession
        """
        data = {
            "title": title,
            "model_name": model,
            "user_id": user_id,
            "message_count": 0,
            "is_pinned": False,
        }
        return await self.chat_repository.create_session(data)

    async def get_session(self, session_id: str) -> ChatSession:
        """
        Get a chat session by ID.

        Args:
            session_id: Session UUID

        Returns:
            ChatSession
        """
        return await self.chat_repository.get_session(uuid.UUID(session_id))

    async def get_sessions(
        self, page: int, size: int, user_id: Optional[str] = None, filters: Optional[dict] = None
    ):
        """
        Get paginated list of chat sessions.

        Args:
            page: Page number (1-indexed)
            size: Page size
            user_id: Optional user filter
            filters: Optional additional filters

        Returns:
            Page object from fastapi_pagination
        """
        params = Params(page=page, size=size)
        if filters is None:
            filters = {}
        if user_id:
            filters["user_id"] = user_id

        result = await self.chat_repository.get_sessions(
            paginate_data=True, page_params=params, filters=filters
        )

        # Ensure we return a proper Page object
        if hasattr(result, "items"):
            return result
        # Fallback: create a proper Page object
        from fastapi_pagination import Page
        return Page(items=result if isinstance(result, list) else [], total=0, page=page, size=size, pages=0)

    async def update_session(self, session_id: str, title: str) -> ChatSession:
        """
        Update a chat session title.

        Args:
            session_id: Session UUID
            title: New title

        Returns:
            Updated ChatSession
        """
        return await self.chat_repository.update_session(
            uuid.UUID(session_id), {"title": title}
        )

    async def delete_session(self, session_id: str) -> bool:
        """
        Delete a chat session.

        Args:
            session_id: Session UUID

        Returns:
            True if deleted
        """
        return await self.chat_repository.delete_session(uuid.UUID(session_id))

    async def send_message(
        self, session_id: str, content: str, model: str, stream: bool = False
    ) -> Message:
        """
        Send a message and get AI response (non-streaming).

        Args:
            session_id: Session UUID
            content: User message content
            model: Model name
            stream: Whether to stream (ignored for this method)

        Returns:
            Assistant Message
        """
        session_uuid = uuid.UUID(session_id)

        # Get session to verify it exists
        _ = await self.chat_repository.get_session(session_uuid)

        # Create user message
        user_message_data = {
            "chat_session_id": session_uuid,
            "role": MessageRole.USER,
            "content": content,
            "model_name": model,
            "is_streaming": False,
        }
        _ = await self.message_repository.create_message(user_message_data)

        # Build conversation history for Ollama
        messages = await self._build_conversation_history(session_uuid)

        # Get AI response
        response = await self.ollama_service.chat_completion(
            messages=messages, model=model, stream=False
        )

        # Extract assistant response
        assistant_content = response.get("message", {}).get("content", "")
        tokens = response.get("eval_count", 0) + response.get("prompt_eval_count", 0)

        # Create assistant message
        assistant_message_data = {
            "chat_session_id": session_uuid,
            "role": MessageRole.ASSISTANT,
            "content": assistant_content,
            "model_name": model,
            "token_count": tokens,
            "is_streaming": False,
        }
        assistant_message = await self.message_repository.create_message(
            assistant_message_data
        )

        # Update session message count
        await self.chat_repository.increment_message_count(session_uuid)

        return assistant_message

    async def send_message_stream(
        self, session_id: str, content: str, model: str
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Send a message and stream AI response.

        Args:
            session_id: Session UUID
            content: User message content
            model: Model name

        Yields:
            Streaming chunks with content, done flag, and model
        """
        session_uuid = uuid.UUID(session_id)

        # Get session to verify it exists
        _ = await self.chat_repository.get_session(session_uuid)

        # Create user message
        user_message_data = {
            "chat_session_id": session_uuid,
            "role": MessageRole.USER,
            "content": content,
            "model_name": model,
            "is_streaming": False,
        }
        _ = await self.message_repository.create_message(user_message_data)

        # Build conversation history
        messages = await self._build_conversation_history(session_uuid)

        # Stream AI response
        accumulated_content = ""
        token_count = 0

        async for chunk in self.ollama_service.chat_completion_stream(
            messages=messages, model=model
        ):
            # Extract content from chunk
            chunk_content = chunk.get("message", {}).get("content", "")
            done = chunk.get("done", False)

            accumulated_content += chunk_content
            if "eval_count" in chunk:
                token_count = chunk["eval_count"]

            yield {
                "content": chunk_content,
                "done": done,
                "model": model,
                "accumulated_content": accumulated_content,
            }

            if done:
                # Create assistant message in database
                assistant_message_data = {
                    "chat_session_id": session_uuid,
                    "role": MessageRole.ASSISTANT,
                    "content": accumulated_content,
                    "model_name": model,
                    "token_count": token_count,
                    "is_streaming": False,
                }
                await self.message_repository.create_message(assistant_message_data)

                # Update session message count
                await self.chat_repository.increment_message_count(session_uuid)

    async def regenerate_message(
        self, session_id: str, message_id: str, model: str
    ) -> Message:
        """
        Regenerate an assistant message.

        Args:
            session_id: Session UUID
            message_id: Message UUID to regenerate (must be assistant message)
            model: Model name

        Returns:
            New assistant Message
        """
        session_uuid = uuid.UUID(session_id)
        message_uuid = uuid.UUID(message_id)

        # Get the message to regenerate
        message = await self.message_repository.get_message(message_uuid)
        if message.role != MessageRole.ASSISTANT:
            raise AppException.BadRequestException(
                error_message="Can only regenerate assistant messages"
            )

        # Delete this message and all messages after it
        _ = await self.message_repository.delete_messages_after(
            session_uuid, message_uuid
        )

        # Build conversation history up to parent message
        messages = await self._build_conversation_history(session_uuid)

        # Get new AI response
        response = await self.ollama_service.chat_completion(
            messages=messages, model=model, stream=False
        )

        # Create new assistant message
        assistant_content = response.get("message", {}).get("content", "")
        tokens = response.get("eval_count", 0) + response.get("prompt_eval_count", 0)

        assistant_message_data = {
            "chat_session_id": session_uuid,
            "role": MessageRole.ASSISTANT,
            "content": assistant_content,
            "model_name": model,
            "token_count": tokens,
            "is_streaming": False,
            "parent_message_id": message.parent_message_id,
        }
        new_message = await self.message_repository.create_message(
            assistant_message_data
        )

        return new_message

    async def get_messages(
        self, session_id: str, page: int, size: int
    ) -> Tuple[List[Message], int]:
        """
        Get paginated messages for a session.

        Args:
            session_id: Session UUID
            page: Page number (1-indexed)
            size: Page size

        Returns:
            Tuple of (messages, total_count)
        """
        params = Params(page=page, size=size)
        result = await self.message_repository.get_messages_by_session(
            uuid.UUID(session_id), paginate_data=True, page_params=params
        )

        if hasattr(result, "items"):
            return result.items, result.total
        return result, len(result) if isinstance(result, list) else 0

    async def _build_conversation_history(self, session_id: uuid.UUID) -> List[Dict[str, str]]:
        """
        Build conversation history for Ollama context.

        Args:
            session_id: Session UUID

        Returns:
            List of message dicts with 'role' and 'content'
        """
        messages = await self.message_repository.get_messages_by_session(
            session_id, paginate_data=False
        )

        history = []
        for msg in messages:
            role = msg.role.value if isinstance(msg.role, MessageRole) else msg.role
            history.append({"role": role, "content": msg.content})

        return history

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models from Ollama."""
        return await self.ollama_service.list_models()

    async def pull_model(self, model_name: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Pull a model from Ollama registry."""
        async for chunk in self.ollama_service.pull_model(model_name):
            yield chunk

    async def check_model_exists(self, model_name: str) -> bool:
        """Check if a model exists in Ollama."""
        return await self.ollama_service.check_model_exists(model_name)

    async def health_check(self) -> Dict[str, Any]:
        """Health check for chat service and Ollama."""
        ollama_healthy = await self.ollama_service.health_check()
        models = []
        if ollama_healthy:
            try:
                models = await self.ollama_service.list_models()
            except Exception:
                pass

        return {
            "status": "healthy" if ollama_healthy else "degraded",
            "ollama_connected": ollama_healthy,
            "models_available": len(models),
        }

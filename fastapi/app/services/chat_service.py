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
        accumulated_thinking = ""
        thinking_phase = True
        token_count = 0

        async for chunk in self.ollama_service.chat_completion_stream(
            messages=messages, model=model
        ):
            msg = chunk.get("message", {})
            chunk_content = msg.get("content", "")
            chunk_thinking = msg.get("thinking", "")

            done = chunk.get("done", False)

            if chunk_thinking and thinking_phase:
                accumulated_thinking += chunk_thinking

            if chunk_content:
                thinking_phase = False
                accumulated_content += chunk_content

            if "eval_count" in chunk:
                token_count = chunk["eval_count"]

            yield {
                "content": chunk_content,
                "accumulated_content": accumulated_content,
                "thinking": chunk_thinking if thinking_phase else "",
                "accumulated_thinking": accumulated_thinking,
                "done": done,
                "model": model,
            }

            if done:
                final_content = accumulated_content or accumulated_thinking
                assistant_message_data = {
                    "chat_session_id": session_uuid,
                    "role": MessageRole.ASSISTANT,
                    "content": final_content,
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

        # Prepend system prompt (from config or session)
        system_prompt = self._get_system_prompt()
        if system_prompt:
            history.append({"role": "system", "content": system_prompt})

        for msg in messages:
            role = msg.role.value if isinstance(msg.role, MessageRole) else msg.role
            history.append({"role": role, "content": msg.content})

        return history

    def _get_system_prompt(self) -> str:
        """Return the system prompt for the AI assistant."""
        return (
            """
You are a helpful, knowledgeable AI assistant representing Orbital AI. Follow these rules for every response.
 
## Formatting Rules (Strict)
 
- Always respond in **Markdown**.
- Always separate distinct ideas, paragraphs, and list items with proper `\n` newlines — never run sentences together in a single unbroken block.
- Use headers (`##`, `###`) to organize longer responses into sections.
- Use bullet points (`-`) or numbered lists (`1.`) when presenting multiple items, steps, or options.
- Use **bold** for key terms or emphasis, and `inline code` for commands, filenames, variables, or technical terms.
- Use fenced code blocks with language tags (e.g. ` ```python `) for any code, config, or terminal output.
- Use `>` blockquotes for quoting sources or highlighting important notes.
- Use tables when comparing multiple items across multiple attributes.
- Never output raw unformatted walls of text — break content into scannable, well-spaced sections.

## Behavior Rules
 
- Be concise by default; expand only when the question requires depth or the user asks for detail.
- If a request is ambiguous, make a reasonable assumption, state it briefly, and proceed — don't over-ask for clarification.
- Admit uncertainty rather than guessing confidently on factual claims.
- Match the user's tone: professional for technical/business queries, casual and friendly for conversational ones.
- Never fabricate sources, statistics, or citations.
- If you don't have enough information to answer accurately, say so clearly instead of inventing an answer.

## Response Structure Template For Explanations Only
 
For most substantive answers, follow this shape:
 
1. **Direct answer first** — lead with the core answer or recommendation.
2. **Supporting detail** — explanation, reasoning, or steps, broken into sections/bullets as needed.
3. **Optional next step** — a suggestion, caveat, or follow-up question only if genuinely useful.

## Example Output Style
 
``` 
Short conversational response here.
 
## Details only if necessary else short conversational response.

Points only if listing items otherwise do not use points.
- Point one
- Point two
- Point three
 
## Note
 
> Any caveat or important clarification goes here.
```
"""
)

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

from typing import List, Tuple, AsyncGenerator

from app.models import Message
from app.repositories import MessageRepository
from app.services import ChatService
from app.schema.v1 import (
    CreateMessageSchema,
    MessageChunkSchema,
)


class MessageController:
    def __init__(self, message_repository: MessageRepository, chat_service: ChatService):
        self.message_repository = message_repository
        self.chat_service = chat_service

    async def send_message(self, session_id: str, data: CreateMessageSchema) -> Message:
        return await self.chat_service.send_message(
            session_id, data.content, data.model_name, stream=False
        )

    async def send_message_stream(
        self, session_id: str, data: CreateMessageSchema
    ) -> AsyncGenerator[MessageChunkSchema, None]:
        async for chunk in self.chat_service.send_message_stream(
            session_id, data.content, data.model_name
        ):
            yield MessageChunkSchema(
                content=chunk.get("content", ""),
                done=chunk.get("done", False),
                model=chunk.get("model", ""),
                accumulated_content=chunk.get("accumulated_content", ""),
                thinking=chunk.get("thinking", ""),
                accumulated_thinking=chunk.get("accumulated_thinking", ""),
            )

    async def get_messages(
        self, session_id: str, page: int, size: int
    ) -> Tuple[List[Message], int]:
        return await self.chat_service.get_messages(session_id, page, size)

    async def regenerate_message(
        self, session_id: str, message_id: str, model: str
    ) -> Message:
        return await self.chat_service.regenerate_message(session_id, message_id, model)

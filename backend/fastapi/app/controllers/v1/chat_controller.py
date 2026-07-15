from typing import List, Optional, Tuple
from fastapi_pagination import Params

from app.models import ChatSession
from app.repositories import ChatRepository
from app.services import ChatService
from app.schema.v1 import (
    CreateChatSessionSchema,
    UpdateChatSessionSchema,
)


class ChatController:
    def __init__(self, chat_repository: ChatRepository, chat_service: ChatService):
        self.chat_repository = chat_repository
        self.chat_service = chat_service

    async def create_session(self, data: CreateChatSessionSchema) -> ChatSession:
        return await self.chat_service.create_session(
            title=data.title,
            model=data.model_name,
            user_id="default",
        )

    async def get_sessions(
        self, page: int = 1, size: int = 20, pinned: Optional[bool] = None
    ):
        page_params = Params(page=page, size=size)
        filters = {}
        if pinned is not None:
            filters["is_pinned"] = pinned
        filters["user_id"] = "default"
        return await self.chat_service.get_sessions(page=page, size=size, user_id="default", filters=filters)

    async def get_session(self, session_id: str) -> ChatSession:
        return await self.chat_service.get_session(session_id)

    async def update_session(self, session_id: str, data: UpdateChatSessionSchema) -> ChatSession:
        return await self.chat_service.update_session(session_id, data.title)

    async def delete_session(self, session_id: str) -> bool:
        return await self.chat_service.delete_session(session_id)

    async def pin_session(self, session_id: str, pinned: bool = True) -> ChatSession:
        return await self.chat_service.update_session(session_id, {"is_pinned": pinned})

    async def get_pinned_sessions(self, limit: int = 20) -> List[ChatSession]:
        return await self.chat_repository.get_pinned_sessions(limit=limit, user_id="default")

    async def get_recent_sessions(self, limit: int = 20) -> List[ChatSession]:
        return await self.chat_repository.get_recent_sessions(limit=limit, user_id="default")

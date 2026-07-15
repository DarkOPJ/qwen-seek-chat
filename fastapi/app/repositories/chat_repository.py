from typing import List, Optional, Dict, Any
import uuid

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
import sqlalchemy as sql
from sqlalchemy import select, func, update as sqlalchemy_update

from app.core.repository import AsyncSQLBaseRepository
from app.models import ChatSession, Message
from app.core.exceptions import AppException


class ChatRepository(AsyncSQLBaseRepository):
    model = ChatSession
    object_name = "chat_session"

    async def create_session(self, data: Dict[str, Any]) -> ChatSession:
        return await self.create(data)

    async def get_session(self, session_id: uuid.UUID) -> ChatSession:
        return await self.find_by_id(session_id)

    async def get_sessions(
        self,
        paginate_data: bool = False,
        page_params: Params = None,
        filters: Optional[Dict[str, Any]] = None,
    ):
        async with self.db_session() as session:
            stmt = select(self.model)
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key):
                        stmt = stmt.where(getattr(self.model, key) == value)
            stmt = stmt.order_by(self.model.created_at.desc())
            return await self._result(
                conn=session,
                query=stmt,
                paginated=paginate_data,
                page_params=page_params,
            )

    async def update_session(
        self, session_id: uuid.UUID, data: Dict[str, Any]
    ) -> ChatSession:
        return await self.update_by_id(session_id, data)

    async def delete_session(self, session_id: uuid.UUID) -> bool:
        return await self.delete_by_id(session_id)

    async def increment_message_count(self, session_id: uuid.UUID) -> ChatSession:
        async with self.db_session() as session:
            # Use a simpler approach compatible with SQLite
            stmt = (
                sqlalchemy_update(self.model)
                .where(self.model.id == session_id)
                .values(message_count=self.model.message_count + 1)
            )
            await session.execute(stmt)
            await session.commit()
            # Fetch the updated session
            updated = await session.get(self.model, session_id)
            if not updated:
                raise AppException.NotFoundException(
                    error_message=f"{self.object_name}({session_id}) not found"
                )
            return updated

    async def get_pinned_sessions(
        self, limit: int = 20, user_id: Optional[str] = None
    ) -> List[ChatSession]:
        async with self.db_session() as session:
            stmt = (
                select(self.model)
                .where(self.model.is_pinned == True)
                .order_by(self.model.updated_at.desc())
                .limit(limit)
            )
            if user_id:
                stmt = stmt.where(self.model.user_id == user_id)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_recent_sessions(
        self, limit: int = 20, user_id: Optional[str] = None
    ) -> List[ChatSession]:
        async with self.db_session() as session:
            stmt = (
                select(self.model)
                .order_by(self.model.updated_at.desc())
                .limit(limit)
            )
            if user_id:
                stmt = stmt.where(self.model.user_id == user_id)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_session_count(self, user_id: Optional[str] = None) -> int:
        async with self.db_session() as session:
            stmt = select(func.count(self.model.id))
            if user_id:
                stmt = stmt.where(self.model.user_id == user_id)
            result = await session.execute(stmt)
            return result.scalar() or 0
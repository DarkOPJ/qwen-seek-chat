from typing import List, Optional
from uuid import UUID

import sqlalchemy as sql
from sqlalchemy import func, select, and_ as sql_and_
from sqlalchemy import delete as sqlalchemy_delete
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate

from app.core.database import db_async_session
from app.core.exceptions import AppException
from app.core.repository import AsyncSQLBaseRepository
from app.models import Message, MessageRole


class MessageRepository(AsyncSQLBaseRepository):
    model = Message
    object_name = "message"

    async def create_message(self, data: dict) -> Message:
        return await self.create(data)

    async def get_message(self, message_id: UUID) -> Message:
        return await self.find_by_id(message_id)

    async def get_messages_by_session(
        self,
        session_id: UUID,
        paginate_data: bool = False,
        page_params: Params = None,
    ):
        async with self.db_session() as session:
            stmt = (
                sql.select(self.model)
                .where(self.model.chat_session_id == session_id)
                .order_by(self.model.created_at)
            )
            return await self._result(
                conn=session,
                query=stmt,
                paginated=paginate_data,
                page_params=page_params,
            )

    async def update_message(self, message_id: UUID, data: dict) -> Message:
        return await self.update_by_id(message_id, data)

    async def delete_message(self, message_id: UUID) -> bool:
        return await self.delete_by_id(message_id)

    async def delete_messages_after(
        self,
        session_id: UUID,
        message_id: UUID,
    ) -> int:
        async with self.db_session() as session:
            # First get the created_at of the message_id
            stmt = select(self.model.created_at).where(self.model.id == message_id)
            result = await session.execute(stmt)
            message_created_at = result.scalar_one_or_none()

            if not message_created_at:
                raise AppException.NotFoundException(
                    error_message=f"{self.object_name}({message_id}) not found"
                )

            # Delete all messages in the same session after the given message
            delete_stmt = sqlalchemy_delete(self.model).where(
                sql_and_(
                    self.model.chat_session_id == session_id,
                    self.model.created_at > message_created_at,
                )
            )
            result = await session.execute(delete_stmt)
            await session.commit()
            return result.rowcount

    async def get_last_message(self, session_id: UUID) -> Optional[Message]:
        async with self.db_session() as session:
            stmt = (
                select(self.model)
                .where(self.model.chat_session_id == session_id)
                .order_by(self.model.created_at.desc())
                .limit(1)
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def count_messages(self, session_id: UUID) -> int:
        async with self.db_session() as session:
            stmt = select(func.count(self.model.id)).where(
                self.model.chat_session_id == session_id
            )
            result = await session.execute(stmt)
            return result.scalar() or 0

    async def get_messages_by_role(
        self, session_id: UUID, role: MessageRole
    ) -> List[Message]:
        async with self.db_session() as session:
            stmt = (
                select(self.model)
                .where(
                    sql_and_(
                        self.model.chat_session_id == session_id,
                        self.model.role == role,
                    )
                )
                .order_by(self.model.created_at.asc())
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_streaming_message(self, session_id: UUID) -> Optional[Message]:
        """Get the currently streaming message for a session."""
        async with self.db_session() as session:
            stmt = (
                select(self.model)
                .where(
                    sql_and_(
                        self.model.chat_session_id == session_id,
                        self.model.is_streaming == True,
                    )
                )
                .order_by(self.model.created_at.desc())
                .limit(1)
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_message_tree(self, session_id: UUID) -> List[Message]:
        """Get all messages for a session ordered by created_at for tree reconstruction."""
        async with self.db_session() as session:
            stmt = (
                select(self.model)
                .where(self.model.chat_session_id == session_id)
                .order_by(self.model.created_at.asc())
            )
            result = await session.execute(stmt)
            return result.scalars().all()
import uuid

from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

from .base_model import BaseModel


class ResourceModel(Base, BaseModel):
    __tablename__ = "resources"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


class BaseModel:
    created_at: Mapped[datetime] = mapped_column(
        nullable=True, server_default=sa.func.now()
    )
    created_by: Mapped[str] = mapped_column(nullable=True)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
    updated_by: Mapped[str] = mapped_column(nullable=True)
    is_deleted: Mapped[bool] = mapped_column(nullable=False, default=False)
    deleted_by: Mapped[str] = mapped_column(nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(nullable=True)

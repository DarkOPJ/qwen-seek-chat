import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ResourceSchema(BaseModel):
    id: uuid.UUID
    name: str
    status: str
    created_at: datetime
    created_by: Optional[str]
    updated_at: Optional[datetime]
    updated_by: Optional[str]
    is_deleted: bool
    deleted_by: Optional[str]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


class CreateResourceSchema(BaseModel):
    name: str
    status: str


class UpdateResourceSchema(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None

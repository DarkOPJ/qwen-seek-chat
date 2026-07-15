import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatSessionSchema(BaseModel):
    """Chat session response schema."""

    id: uuid.UUID
    title: Optional[str]
    model_name: str
    user_id: Optional[str]
    is_pinned: bool
    message_count: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class CreateChatSessionSchema(BaseModel):
    """Create chat session request schema."""

    title: str = Field(..., min_length=1, max_length=255)
    model_name: str = Field(default="qwen3:1.7b", min_length=1, max_length=100)


class UpdateChatSessionSchema(BaseModel):
    """Update chat session request schema."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)


class MessageSchema(BaseModel):
    """Message response schema."""

    id: uuid.UUID
    session_id: uuid.UUID
    role: str
    content: str
    model_name: str
    token_count: Optional[int]
    is_streaming: bool
    parent_message_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class CreateMessageSchema(BaseModel):
    """Create message request schema."""

    content: str = Field(..., min_length=1)
    model_name: str = Field(default="qwen3:1.7b", min_length=1, max_length=100)


class MessageChunkSchema(BaseModel):
    """Streaming message chunk schema."""

    content: str
    done: bool
    model: str
    accumulated_content: Optional[str] = None


class ChatCompletionRequest(BaseModel):
    """OpenAI-compatible chat completion request."""

    messages: List[dict] = Field(..., min_items=1)
    model: str
    stream: bool = False
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1)
    top_p: Optional[float] = Field(default=1.0, ge=0.0, le=1.0)
    frequency_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0)
    presence_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0)
    stop: Optional[List[str]] = None


class ChatCompletionChoice(BaseModel):
    """OpenAI-compatible chat completion choice."""

    index: int
    message: dict
    finish_reason: Optional[str] = None


class ChatCompletionUsage(BaseModel):
    """OpenAI-compatible chat completion usage."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    """OpenAI-compatible chat completion response."""

    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: ChatCompletionUsage


class ChatCompletionStreamChoice(BaseModel):
    """OpenAI-compatible streaming choice."""

    index: int
    delta: dict
    finish_reason: Optional[str] = None


class ChatCompletionStreamResponse(BaseModel):
    """OpenAI-compatible streaming response."""

    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[ChatCompletionStreamChoice]


class ModelInfoSchema(BaseModel):
    """Model information schema."""

    name: str
    size: Optional[int] = None
    modified_at: Optional[datetime] = None
    digest: Optional[str] = None
    details: Optional[dict] = None

    class Config:
        from_attributes = True


class ModelPullProgressSchema(BaseModel):
    """Model pull progress schema."""

    status: str
    digest: Optional[str] = None
    total: Optional[int] = None
    completed: Optional[int] = None


class HealthCheckSchema(BaseModel):
    """Health check response schema."""

    status: str
    ollama_connected: bool
    models_available: int

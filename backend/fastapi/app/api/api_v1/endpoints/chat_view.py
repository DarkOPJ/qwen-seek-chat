import uuid
from typing import Optional

import pinject
from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page, Params

from app.controllers.v1 import ChatController, MessageController
from app.repositories import ChatRepository, MessageRepository
from app.schema.v1 import (
    ChatSessionSchema,
    CreateChatSessionSchema,
    UpdateChatSessionSchema,
    MessageSchema,
    CreateMessageSchema,
)
from app.services import ChatService, OllamaService
from app.utils import get_openapi_responses

chat_router = APIRouter(tags=["Chat"])
chat_base_url = "/chat/api/v1"

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[
        ChatController,
        MessageController,
        ChatRepository,
        MessageRepository,
        ChatService,
        OllamaService,
    ],
)

chat_controller: ChatController = obj_graph.provide(ChatController)
message_controller: MessageController = obj_graph.provide(MessageController)


@chat_router.post(
    "/sessions",
    response_model=ChatSessionSchema,
    responses=get_openapi_responses(400, 422, 500),
    status_code=201,
)
async def create_session(payload: CreateChatSessionSchema):
    """Create a new chat session."""
    return await chat_controller.create_session(payload)


@chat_router.get(
    "/sessions",
    response_model=Page[ChatSessionSchema],
    responses=get_openapi_responses(400, 500),
)
async def get_sessions(
    pagination: Params = Depends(),
    pinned: Optional[bool] = Query(None, description="Filter by pinned status"),
):
    """Get paginated list of chat sessions."""
    return await chat_controller.get_sessions(pagination.page, pagination.size, pinned)


@chat_router.get(
    "/sessions/{session_id}",
    response_model=ChatSessionSchema,
    responses=get_openapi_responses(404, 400, 500),
)
async def get_session(session_id: uuid.UUID):
    """Get a chat session by ID."""
    return await chat_controller.get_session(str(session_id))


@chat_router.patch(
    "/sessions/{session_id}",
    response_model=ChatSessionSchema,
    responses=get_openapi_responses(404, 400, 422, 500),
)
async def update_session(session_id: uuid.UUID, payload: UpdateChatSessionSchema):
    """Update a chat session title."""
    return await chat_controller.update_session(str(session_id), payload)


@chat_router.delete(
    "/sessions/{session_id}",
    status_code=204,
    responses=get_openapi_responses(404, 400, 500),
)
async def delete_session(session_id: uuid.UUID):
    """Delete a chat session."""
    return await chat_controller.delete_session(str(session_id))


@chat_router.post(
    "/sessions/{session_id}/messages",
    response_model=MessageSchema,
    responses=get_openapi_responses(400, 404, 422, 500),
    status_code=201,
)
async def send_message(session_id: uuid.UUID, payload: CreateMessageSchema):
    """Send a message and get AI response (non-streaming)."""
    return await message_controller.send_message(str(session_id), payload)


@chat_router.get(
    "/sessions/{session_id}/messages",
    response_model=Page[MessageSchema],
    responses=get_openapi_responses(400, 404, 500),
)
async def get_messages(session_id: uuid.UUID, pagination: Params = Depends()):
    """Get paginated messages for a session."""
    messages, total = await message_controller.get_messages(
        str(session_id), pagination.page, pagination.size
    )
    return Page.create(messages, total=total, params=pagination)


@chat_router.post(
    "/sessions/{session_id}/messages/{message_id}/regenerate",
    response_model=MessageSchema,
    responses=get_openapi_responses(400, 404, 422, 500),
)
async def regenerate_message(
    session_id: uuid.UUID, message_id: uuid.UUID, model: str = "qwen3:1.7b"
):
    """Regenerate an assistant message."""
    return await message_controller.regenerate_message(
        str(session_id), str(message_id), model
    )

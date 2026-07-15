import json
import uuid
from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from loguru import logger as loguru_logger

from app.controllers.v1 import MessageController
from app.repositories import MessageRepository, ChatRepository
from app.services import ChatService, OllamaService
from app.schema.v1 import MessageChunkSchema, CreateMessageSchema

websocket_router = APIRouter(prefix="/chat/api/v1", tags=["WebSocket Chat"])


class ConnectionManager:
    """Manages active WebSocket connections for chat streaming."""

    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, session_id: str, websocket: WebSocket):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = set()
        self.active_connections[session_id].add(websocket)
        loguru_logger.info(f"WebSocket connected for session {session_id}")

    def disconnect(self, session_id: str, websocket: WebSocket):
        if session_id in self.active_connections:
            self.active_connections[session_id].discard(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]
        loguru_logger.info(f"WebSocket disconnected for session {session_id}")

    async def send_chunk(self, session_id: str, chunk: MessageChunkSchema):
        """Send a streaming chunk to all connections for a session."""
        if session_id in self.active_connections:
            data = chunk.model_dump_json()
            disconnected = set()
            for ws in self.active_connections[session_id]:
                try:
                    await ws.send_text(data)
                except Exception as e:
                    loguru_logger.warning(f"Failed to send to websocket: {e}")
                    disconnected.add(ws)
            for ws in disconnected:
                self.disconnect(session_id, ws)

    async def send_message(self, session_id: str, message: dict):
        """Send a JSON message to all connections for a session."""
        if session_id in self.active_connections:
            data = json.dumps(message)
            disconnected = set()
            for ws in self.active_connections[session_id]:
                try:
                    await ws.send_text(data)
                except Exception as e:
                    loguru_logger.warning(f"Failed to send to websocket: {e}")
                    disconnected.add(ws)
            for ws in disconnected:
                self.disconnect(session_id, ws)


# Singleton connection manager
connection_manager = ConnectionManager()

# Dependency injection setup
import pinject
obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[
        MessageController,
        MessageRepository,
        ChatRepository,
        ChatService,
        OllamaService,
    ],
)

message_controller: MessageController = obj_graph.provide(MessageController)


@websocket_router.websocket("/sessions/{session_id}/stream")
async def websocket_chat_stream(
    websocket: WebSocket,
    session_id: uuid.UUID,
    message_id: uuid.UUID = Query(..., description="User message ID to stream response for"),
    model: str = Query("qwen3:1.7b", description="Model to use for generation"),
):
    """
    WebSocket endpoint for streaming chat responses.

    Query Parameters:
    - message_id: The user message ID that triggered this stream
    - model: Model name to use (default: qwen3:1.7b)

    Message Format (outgoing chunks):
    - {"content": "...", "done": false, "model": "qwen3:1.7b", "accumulated_content": "..."}
    - Final: {"content": "", "done": true, "model": "qwen3:1.7b", "message_id": "...", "tokens": 123}
    """
    session_id_str = str(session_id)

    await connection_manager.connect(session_id_str, websocket)

    try:
        # Get the user message content from the database
        message_repo = MessageRepository()
        user_message = await message_repo.get_message(message_id)

        if not user_message:
            await websocket.send_json({
                "content": "",
                "done": True,
                "model": model,
                "error": "User message not found",
            })
            return

        if user_message.chat_session_id != session_id:
            await websocket.send_json({
                "content": "",
                "done": True,
                "model": model,
                "error": "Message does not belong to this session",
            })
            return

        # Stream the response using the message controller
        create_schema = CreateMessageSchema(content=user_message.content, model_name=model)

        async for chunk in message_controller.send_message_stream(session_id_str, create_schema):
            await websocket.send_text(chunk.model_dump_json())

    except WebSocketDisconnect:
        loguru_logger.info(f"WebSocket disconnected for session {session_id_str}")
    except Exception as e:
        loguru_logger.error(f"WebSocket error for session {session_id_str}: {e}")
        try:
            await websocket.send_json({
                "content": "",
                "done": True,
                "model": model,
                "error": str(e),
            })
        except Exception:
            pass
    finally:
        connection_manager.disconnect(session_id_str, websocket)

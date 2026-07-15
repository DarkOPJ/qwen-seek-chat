import pinject
from typing import List
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.controllers.v1 import ModelController
from app.services import OllamaService
from app.schema.v1 import ModelInfoSchema, HealthCheckSchema
from app.utils import get_openapi_responses

model_router = APIRouter(prefix="/chat/api/v1", tags=["Models"])

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[ModelController, OllamaService],
)

model_controller: ModelController = obj_graph.provide(ModelController)


@model_router.get(
    "/models",
    response_model=List[ModelInfoSchema],
    responses=get_openapi_responses(500),
)
async def list_models():
    """List all available models in Ollama."""
    return await model_controller.list_models()


@model_router.get(
    "/models/{model_name}",
    response_model=ModelInfoSchema,
    responses=get_openapi_responses(404, 500),
)
async def get_model(model_name: str):
    """Get detailed information about a specific model."""
    return await model_controller.get_model(model_name)


@model_router.post(
    "/models/pull",
    response_model=None,
    responses=get_openapi_responses(400, 404, 500),
)
async def pull_model(model_name: str = Query(..., description="Model name to pull")):
    """Pull a model from Ollama registry (streaming response)."""

    async def generate():
        async for progress in model_controller.pull_model(model_name):
            yield f"data: {progress.model_dump_json()}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@model_router.get(
    "/models/{model_name}/check",
    response_model=bool,
    responses=get_openapi_responses(500),
)
async def check_model(model_name: str):
    """Check if a model exists in Ollama."""
    return await model_controller.check_model(model_name)


@model_router.delete(
    "/models/{model_name}",
    status_code=204,
    responses=get_openapi_responses(404, 500),
)
async def delete_model(model_name: str):
    """Delete a model from Ollama."""
    return await model_controller.delete_model(model_name)


@model_router.get(
    "/health",
    response_model=HealthCheckSchema,
    responses=get_openapi_responses(500),
)
async def health_check():
    """Health check endpoint for chat service and Ollama."""
    from app.services import ChatService
    from app.repositories import ChatRepository, MessageRepository

    chat_repo = ChatRepository()
    message_repo = MessageRepository()
    ollama_service = OllamaService()
    chat_service = ChatService(chat_repo, message_repo, ollama_service)

    return await chat_service.health_check()

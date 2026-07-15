from fastapi import FastAPI

from .endpoints.async_resource_view import async_resource_base_url, async_resource_router
from .endpoints.sync_resource_view import sync_resource_base_url, sync_resource_router
from .endpoints.chat_view import chat_base_url, chat_router
from .endpoints.model_view import model_router
from .endpoints.websocket_chat import websocket_router


def init_api_v1(app: FastAPI):
    app.include_router(
        router=async_resource_router,
        tags=["AsyncResource"],
        prefix=async_resource_base_url,
    )
    app.include_router(
        router=sync_resource_router,
        tags=["SyncResource"],
        prefix=sync_resource_base_url,
    )
    app.include_router(
        router=chat_router,
        tags=["Chat"],
        prefix=chat_base_url,
    )
    app.include_router(
        router=model_router,
        tags=["Models"],
    )
    app.include_router(
        router=websocket_router,
        tags=["WebSocket Chat"],
    )
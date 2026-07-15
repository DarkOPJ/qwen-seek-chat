from typing import List, Dict, Any, AsyncGenerator

from app.schema.v1 import ModelPullProgressSchema
from app.services import OllamaService


class ModelController:
    def __init__(self, ollama_service: OllamaService):
        self.ollama_service = ollama_service

    async def list_models(self) -> List[Dict[str, Any]]:
        return await self.ollama_service.list_models()

    async def get_model(self, model_name: str) -> Dict[str, Any]:
        return await self.ollama_service.get_model_info(model_name)

    async def pull_model(self, model_name: str) -> AsyncGenerator[ModelPullProgressSchema, None]:
        async for progress in self.ollama_service.pull_model(model_name):
            yield ModelPullProgressSchema(
                status=progress.get("status", ""),
                digest=progress.get("digest"),
                total=progress.get("total"),
                completed=progress.get("completed"),
            )

    async def check_model(self, model_name: str) -> bool:
        return await self.ollama_service.check_model_exists(model_name)

    async def delete_model(self, model_name: str) -> bool:
        return await self.ollama_service.delete_model(model_name)

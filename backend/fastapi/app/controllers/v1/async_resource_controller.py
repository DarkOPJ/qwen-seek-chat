from typing import List

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate

from app.models import ResourceModel
from app.repositories import AsyncResourceRepository


class AsyncResourceController:
    def __init__(self, async_resource_repository: AsyncResourceRepository):
        self.resource_repository = async_resource_repository

    async def create_resource(self, obj_data: dict) -> ResourceModel:
        return await self.resource_repository.create(obj_data)

    async def get_all_resources(self, page_params: Params) -> List[paginate]:
        return await self.resource_repository.index(
            paginate_data=True, page_params=page_params
        )

    async def get_resource(self, obj_id: str):
        return await self.resource_repository.find_by_id(obj_id=obj_id)

    async def update_resource(self, obj_id: str, obj_data: dict):
        return await self.resource_repository.update_by_id(
            obj_id=obj_id, obj_in=obj_data
        )

    async def delete_resource(self, obj_id: str):
        await self.resource_repository.delete_by_id(obj_id=obj_id)
        return None

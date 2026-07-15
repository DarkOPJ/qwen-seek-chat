from typing import List

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate

from app.models import ResourceModel
from app.repositories import SyncResourceRepository


class SyncResourceController:
    def __init__(self, sync_resource_repository: SyncResourceRepository):
        self.resource_repository = sync_resource_repository

    def create_resource(self, obj_data: dict) -> ResourceModel:
        return self.resource_repository.create(obj_data)

    def get_all_resources(self, page_params: Params) -> List[paginate]:
        return self.resource_repository.index(
            paginate_data=True, page_params=page_params
        )

    def get_resource(self, obj_id: str):
        return self.resource_repository.find_by_id(obj_id=obj_id)

    def update_resource(self, obj_id: str, obj_data: dict):
        return self.resource_repository.update_by_id(obj_id=obj_id, obj_in=obj_data)

    def delete_resource(self, obj_id: str):
        self.resource_repository.delete_by_id(obj_id=obj_id)
        return None

import uuid

import pinject
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from app.controllers.v1 import SyncResourceController
from app.repositories import SyncResourceRepository
from app.schema.v1 import CreateResourceSchema, ResourceSchema, UpdateResourceSchema
from app.services import RedisService
from app.utils import get_openapi_responses

sync_resource_router = APIRouter()
sync_resource_base_url = "/sync/resource/api/v1"

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[SyncResourceController, SyncResourceRepository, RedisService],
)

resource_controller: SyncResourceController = obj_graph.provide(SyncResourceController)


@sync_resource_router.post(
    "/new",
    response_model=ResourceSchema,
    responses=get_openapi_responses(400, 422, 500),
    status_code=201,
)
def create_resource(payload: CreateResourceSchema):
    return resource_controller.create_resource(obj_data=payload.model_dump())


@sync_resource_router.get("/all", response_model=Page[ResourceSchema])
def get_all_resource(pagination: Params = Depends()):  # noqa
    return resource_controller.get_all_resources(page_params=pagination)


@sync_resource_router.get("/get/{resource_id}", response_model=ResourceSchema)
def get_resource(resource_id: uuid.UUID):
    return resource_controller.get_resource(obj_id=str(resource_id))


@sync_resource_router.patch("/update/{resource_id}", response_model=ResourceSchema)
def update_resource(resource_id: uuid.UUID, payload: UpdateResourceSchema):
    return resource_controller.update_resource(
        obj_id=str(resource_id), obj_data=payload.model_dump(exclude_unset=True)
    )


@sync_resource_router.delete("/delete/{resource_id}", status_code=204)
def delete_resource(resource_id: uuid.UUID):
    return resource_controller.delete_resource(obj_id=str(resource_id))

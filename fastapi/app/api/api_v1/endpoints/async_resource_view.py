import uuid

import pinject
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from app.controllers.v1 import AsyncResourceController
from app.repositories import AsyncResourceRepository
from app.schema.v1 import CreateResourceSchema, ResourceSchema, UpdateResourceSchema
from app.services import RedisService
from app.utils import get_openapi_responses

async_resource_router = APIRouter()
async_resource_base_url = "/async/resource/api/v1"

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[AsyncResourceController, AsyncResourceRepository, RedisService],
)

resource_controller: AsyncResourceController = obj_graph.provide(
    AsyncResourceController
)


@async_resource_router.post(
    "/new",
    response_model=ResourceSchema,
    responses=get_openapi_responses(400, 422, 500),
    status_code=201,
)
async def create_resource(payload: CreateResourceSchema):
    return await resource_controller.create_resource(obj_data=payload.model_dump())


@async_resource_router.get("/all", response_model=Page[ResourceSchema])
async def get_all_resource(pagination: Params = Depends()):  # noqa
    return await resource_controller.get_all_resources(page_params=pagination)


@async_resource_router.get("/get/{resource_id}", response_model=ResourceSchema)
async def get_resource(resource_id: uuid.UUID):
    return await resource_controller.get_resource(obj_id=str(resource_id))


@async_resource_router.patch("/update/{resource_id}", response_model=ResourceSchema)
async def update_resource(resource_id: uuid.UUID, payload: UpdateResourceSchema):
    return await resource_controller.update_resource(
        obj_id=str(resource_id), obj_data=payload.model_dump(exclude_unset=True)
    )


@async_resource_router.delete("/delete/{resource_id}", status_code=204)
async def delete_resource(resource_id: uuid.UUID):
    return await resource_controller.delete_resource(obj_id=str(resource_id))

import pytest
from fastapi_pagination import Params

from app.models import ResourceModel
from tests.async_base_test_case import AsyncBaseTestCase


class TestAsyncResourceController(AsyncBaseTestCase):
    @pytest.mark.a_sync
    async def test_get_all_resource(self):
        result = await self.resource_controller.get_all_resources(page_params=Params())
        self.assertTrue(result)
        self.assertIsInstance(result.items, list)
        self.assertTrue(all(isinstance(obj, ResourceModel) for obj in result.items))

    @pytest.mark.a_sync
    async def test_get_a_resource(self):
        result = await self.resource_controller.get_resource(
            obj_id=self.resource_model.id
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, ResourceModel)

    @pytest.mark.a_sync
    async def test_create_resource(self):
        result = await self.resource_controller.create_resource(
            obj_data=self.resource_test_data.add_resource
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, ResourceModel)

    @pytest.mark.a_sync
    async def test_update_resource(self):
        result = await self.resource_controller.update_resource(
            obj_id=self.resource_model.id,
            obj_data=self.resource_test_data.update_resource,
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, ResourceModel)

    @pytest.mark.a_sync
    async def test_delete_resource(self):
        result = await self.resource_controller.delete_resource(
            obj_id=self.resource_model.id
        )
        self.assertIsNone(result)

import pytest

from app.api.api_v1.endpoints import async_resource_base_url
from tests.async_base_test_case import AsyncBaseTestCase


class TestResourceAsyncView(AsyncBaseTestCase):
    @pytest.mark.a_sync
    async def test_create_resource(self):
        with self.test_client as test_client:
            response = test_client.post(
                f"{async_resource_base_url}/new",
                json=self.resource_test_data.add_resource,
            )
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)

    @pytest.mark.a_sync
    async def test_get_all_resource(self):
        with self.test_client as test_client:
            response = test_client.get(f"{async_resource_base_url}/all")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)

    @pytest.mark.a_sync
    async def test_get_a_resource(self):
        with self.test_client as test_client:
            response = test_client.get(
                f"{async_resource_base_url}/get/{self.resource_model.id}",
            )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)

    @pytest.mark.a_sync
    async def test_update_resource(self):
        with self.test_client as test_client:
            response = test_client.patch(
                f"{async_resource_base_url}/update/{self.resource_model.id}",
                json=self.resource_test_data.update_resource,
            )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)

    @pytest.mark.a_sync
    async def test_delete_resource(self):
        with self.test_client as test_client:
            response = test_client.delete(
                f"{async_resource_base_url}/delete/{self.resource_model.id}"
            )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(response.content)

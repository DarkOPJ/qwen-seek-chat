import pytest

from app.api.api_v1.endpoints import sync_resource_base_url
from tests.base_test_case import BaseTestCase


class TestResourceSyncView(BaseTestCase):
    @pytest.mark.sync
    def test_create_resource(self, test_app):
        with test_app as test_client:
            response = test_client.post(
                f"{sync_resource_base_url}/new",
                json=self.resource_test_data.add_resource,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 201
        assert isinstance(response_data, dict)

    @pytest.mark.sync
    def test_get_all_resources(self, test_app):
        with test_app as test_client:
            response = test_client.get(f"{sync_resource_base_url}/all")
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.sync
    def test_get_a_resource(self, test_app):
        with test_app as test_client:
            response = test_client.get(
                f"{sync_resource_base_url}/get/{self.resource_model.id}"
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.sync
    def test_update_resource(self, test_app):
        with test_app as test_client:
            response = test_client.patch(
                f"{sync_resource_base_url}/update/{self.resource_model.id}",
                json=self.resource_test_data.update_resource,
            )
        response_data = response.json()
        assert response_data
        assert response.status_code == 200
        assert isinstance(response_data, dict)

    @pytest.mark.sync
    def test_delete_resource(self, test_app):
        with test_app as test_client:
            response = test_client.delete(
                f"{sync_resource_base_url}/delete/{self.resource_model.id}"
            )
        assert response.status_code == 204
        assert not response.content

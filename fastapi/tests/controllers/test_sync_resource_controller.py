import pytest
from fastapi_pagination import Params

from app.models import ResourceModel
from tests.base_test_case import BaseTestCase


class TestResourceController(BaseTestCase):
    @pytest.mark.sync
    def test_get_all_resource(self, test_app):
        result = self.resource_controller.get_all_resources(page_params=Params())
        assert result
        assert isinstance(result.items, list)
        assert all(isinstance(obj, ResourceModel) for obj in result.items)

    @pytest.mark.sync
    def test_get_a_resource(self, test_app):
        result = self.resource_controller.get_resource(obj_id=self.resource_model.id)
        assert result
        assert isinstance(result, ResourceModel)

    @pytest.mark.sync
    def test_create_resource(self, test_app):
        result = self.resource_controller.create_resource(
            obj_data=self.resource_test_data.add_resource
        )
        assert result
        assert isinstance(result, ResourceModel)

    @pytest.mark.sync
    def test_update_resource(self, test_app):
        result = self.resource_controller.update_resource(
            obj_id=self.resource_model.id,
            obj_data=self.resource_test_data.update_resource,
        )
        assert result
        assert isinstance(result, ResourceModel)

    @pytest.mark.sync
    def test_delete_resource(self, test_app):
        result = self.resource_controller.delete_resource(obj_id=self.resource_model.id)
        assert result is None

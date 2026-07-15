import pytest

from app.models import ResourceModel
from tests.base_test_case import BaseTestCase, db_sync_session


class TestResourceSyncModel(BaseTestCase):
    @pytest.mark.sync
    def test_resource_sync_model(self, test_app):
        with db_sync_session() as db_session:
            result = db_session.query(ResourceModel).get(self.resource_model.id)
        assert result
        assert hasattr(result, "id")
        assert hasattr(result, "name")
        assert hasattr(result, "status")
        assert hasattr(result, "created_at")
        assert hasattr(result, "created_by")
        assert hasattr(result, "updated_at")
        assert hasattr(result, "updated_by")
        assert hasattr(result, "is_deleted")
        assert hasattr(result, "deleted_at")
        assert hasattr(result, "deleted_by")

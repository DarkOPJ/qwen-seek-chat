import pytest

from app.models import ResourceModel
from tests.async_base_test_case import AsyncBaseTestCase, db_async_session


class TestResourceAsyncModel(AsyncBaseTestCase):
    @pytest.mark.a_sync
    async def test_resource_async_model(self):
        async with db_async_session() as db_session:
            result = await db_session.get(ResourceModel, self.resource_model.id)
        self.assertTrue(result)
        self.assertTrue(hasattr(result, "id"))
        self.assertTrue(hasattr(result, "name"))
        self.assertTrue(hasattr(result, "status"))
        self.assertTrue(hasattr(result, "created_at"))
        self.assertTrue(hasattr(result, "created_by"))
        self.assertTrue(hasattr(result, "updated_at"))
        self.assertTrue(hasattr(result, "updated_by"))
        self.assertTrue(hasattr(result, "is_deleted"))
        self.assertTrue(hasattr(result, "deleted_at"))
        self.assertTrue(hasattr(result, "deleted_by"))

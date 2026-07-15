from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from fastapi.testclient import TestClient

from app import constants, create_app
from app.controllers import AsyncResourceController
from app.core.database import Base, db_async_session, db_engine
from app.models import ResourceModel
from app.repositories import AsyncResourceRepository
from app.services import RedisService
from app.utils import validate_environment
from tests.data import ResourceTestData
from tests.utils import MockSideEffects


class AsyncBaseTestCase(IsolatedAsyncioTestCase, MockSideEffects):
    def create_app(self):
        validate_environment(modes=[constants.TESTING_ENVIRONMENT])
        app = create_app()
        return app

    def instantiate_classes(self):
        self.redis_service = RedisService()
        self.resource_repository = AsyncResourceRepository()
        self.resource_controller = AsyncResourceController(self.resource_repository)

    def setup_patches(self):
        bug_report = patch("app.core.log.MailHandler.send_mail")
        self.addCleanup(bug_report.stop)
        bug_report.start()

    def setUp(self):
        """
        Will be called before every test
        """
        self.instantiate_classes()
        self.redis_service.get_client().flushdb()
        self.setup_patches()
        self.test_client = TestClient(self.create_app())

    async def _create_tables(self):
        async with db_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def _drop_tables(self):
        async with db_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def commit_data_model(self, model):
        async with db_async_session() as db_session:
            db_session.add(model)
            await db_session.commit()
            await db_session.refresh(model)

    async def setup_async_test_data(self):
        await self._create_tables()
        self.resource_test_data = ResourceTestData()
        self.resource_model = ResourceModel(**self.resource_test_data.existing_resource)
        await self.commit_data_model(self.resource_model)

    async def setup_async_patches(self):
        pass

    async def asyncSetUp(self):
        await self._drop_tables()
        await self.setup_async_test_data()
        await self.setup_async_patches()

    def tearDown(self):
        """
        Will be called after every test
        """
        self.redis_service.get_client().flushdb()

    async def asyncTearDown(self):
        await self._drop_tables()

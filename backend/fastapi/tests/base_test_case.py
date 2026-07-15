import pytest
from fastapi.testclient import TestClient

from app import constants
from app.controllers import SyncResourceController
from app.core.database import Base, db_engine, db_sync_session
from app.models import ResourceModel
from app.repositories import SyncResourceRepository
from app.utils import validate_environment
from tests.data import ResourceTestData
from tests.utils import MockSideEffects


@pytest.mark.usefixtures("app")
class BaseTestCase(MockSideEffects):
    @pytest.fixture
    def test_app(self, app, redis_instance, mocker):
        validate_environment(modes=[constants.TESTING_ENVIRONMENT])
        Base.metadata.drop_all(bind=db_engine)
        redis_instance.get_client().flushdb()
        test_client = TestClient(app)
        self.setup_test_data()
        self.setup_patches(mocker)
        self.instantiate_classes()
        yield test_client
        Base.metadata.drop_all(bind=db_engine)
        redis_instance.get_client().flushdb()

    def setup_test_data(self):
        Base.metadata.create_all(bind=db_engine)
        self.resource_test_data = ResourceTestData()
        self.resource_model = ResourceModel(**self.resource_test_data.existing_resource)
        self.commit_data_model(self.resource_model)

    def commit_data_model(self, model):
        with db_sync_session() as db_session:
            db_session.add(model)
            db_session.commit()
            db_session.refresh(model)

    def instantiate_classes(self):
        self.resource_repository = SyncResourceRepository()
        self.resource_controller = SyncResourceController(
            sync_resource_repository=self.resource_repository
        )

    def setup_patches(self, mocker, **kwargs):
        mocker.patch("app.core.log.MailHandler.send_mail")

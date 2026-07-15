import pytest
from fakeredis import aioredis

from app import create_app
from app.services import RedisService


@pytest.fixture
def app():
    app = create_app(rate_limit_backend=aioredis.FakeRedis())
    yield app


@pytest.fixture
def redis_instance():
    redis = RedisService()
    yield redis

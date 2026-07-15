from typing import Any

from loguru import logger as loguru_logger
from redis.exceptions import RedisError

from app.core.exceptions import exception_message
from app.core.service_interfaces import CacheServiceInterface
from app.providers import RedisGenericProvider, RedisSentinelProvider
from config import settings


class RedisService(CacheServiceInterface):
    def __init__(self):
        if settings.redis_sentinel:
            self.redis = RedisSentinelProvider()
        else:
            self.redis = RedisGenericProvider()

    def _exec_command(self, operation: str, *args, **kwargs):
        """Execute a Redis command safely with error logging."""
        try:
            return getattr(self.redis, operation)(*args, **kwargs)
        except RedisError as exc:
            loguru_logger.critical(
                exception_message(error="RedisError", message=str(exc))
            )
            return None

    def set(self, name: str, value: str, ex: int = None):
        result = self._exec_command(
            "set", self.stringify(name), self.stringify(value), ex=ex
        )
        return result is not None

    def get(self, name: str):
        return self._exec_command("get", self.stringify(name))

    def delete(self, name: str):
        result = self._exec_command("delete", self.stringify(name))
        return result is not None

    def get_client(self):
        return self.redis.get_client()

    # noinspection PyMethodMayBeStatic
    def stringify(self, key: Any):
        return str(key) if not isinstance(key, str) else key

import redis
from redis.sentinel import Sentinel

from app.core.service_interfaces import CacheServiceInterface
from config import settings


class RedisGenericProvider(CacheServiceInterface):
    def __init__(self):
        self.redis_conn = redis.Redis(
            host=settings.redis_server,
            port=settings.redis_port,
            db=settings.redis_db,
            password=f"{settings.redis_password}",
            decode_responses=True,
        )

    def set(self, name: str, value: str, ex: int = None):
        self.redis_conn.set(name=name, value=value, ex=ex)

    def get(self, name: str):
        return self.redis_conn.get(name)

    def delete(self, name: str):
        self.redis_conn.delete(name)

    def get_client(self):
        return self.redis_conn


class RedisSentinelProvider(CacheServiceInterface):
    def __init__(self):
        self.sentinels = settings.redis_sentinel.split("|")
        self.password = settings.redis_password
        self.timeout = settings.redis_sentinel_timeout
        self.master_name = settings.redis_sentinel_master
        self.redis_conn = Sentinel(
            [tuple(sentinel.split(":")) for sentinel in self.sentinels],
            sentinel_kwargs={"password": self.password},
            socket_timeout=settings.redis_sentinel_timeout,
            decode_responses=True,
        )

    def set(self, name: str, value: str, ex: int = None):
        master = self.redis_conn.master_for(
            self.master_name,
            password=self.password,
            socket_timeout=self.timeout,
            db=settings.redis_db,
        )
        master.set(name=name, value=value, ex=ex)

    def get(self, name: str):
        slave = self.redis_conn.slave_for(
            self.master_name,
            password=self.password,
            socket_timeout=self.timeout,
            db=settings.redis_db,
        )
        return slave.get(name)

    def delete(self, name: str):
        master = self.redis_conn.master_for(
            self.master_name,
            password=self.password,
            socket_timeout=self.timeout,
            db=settings.redis_db,
        )
        master.delete(name)

    def get_client(self):
        return self.redis_conn.master_for(
            self.master_name,
            password=self.password,
            socket_timeout=self.timeout,
            db=settings.redis_db,
        )

from abc import ABC, abstractmethod

import redis

from settings import settings


class Cache(ABC):

    @abstractmethod
    def set_cache(self, key: str, value) -> None:
        pass

    @abstractmethod
    def get_cache(self, key: str):
        pass


class RedisCache(Cache):
    TTL_SECONDS = 60 * 5

    def __init__(self):
        self._client = redis.Redis(
            port=settings.REDIS_PORT
        )
        self._health_check()

    def _health_check(self):
        ping = self._client.ping()
        if ping is False:
            raise redis.ConnectionError()

    def set_cache(self, key: str, value: str | bytes) -> None:
        self._client.set(key, value, ex=self.TTL_SECONDS)

    def get_cache(self, key: str) -> str:
        return self._client.get(key)

import redis

from settings import settings


class RedisClient:
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

    def set_cache(self, key: str, value) -> None:
        self._client.set(key, value, ex=self.TTL_SECONDS)

    def get_cache(self, key: str):
        return self._client.get(key)

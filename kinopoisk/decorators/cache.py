from functools import wraps
from typing import Type

from pydantic import BaseModel
import orjson

from kinopoisk.services.cache import RedisCache


def cache(instance_class: Type[BaseModel], many: bool = False):
    def decorator(func):
        @wraps(func)
        def wrapper_func(*args, **kwargs):
            cache_service = RedisCache()
            key = _build_key(instance_class, kwargs.get('id'))
            cached_value = cache_service.get_cache(key)
            if cached_value:
                if not many:
                    return instance_class.parse_raw(cached_value)
                return [instance_class.parse_raw(i) for i in orjson.loads(cached_value)]

            result = func(*args, **kwargs)

            value_to_cache = result.json() if not many else orjson.dumps([i.json() for i in result])
            cache_service.set_cache(key, value_to_cache)
            return result
        return wrapper_func
    return decorator


def _build_key(instance_class: Type[BaseModel], id_: str | None) -> str:
    if not id_:
        return f'{instance_class.__name__} all'
    return f'{instance_class.__name__} {id_}'

from functools import wraps

from kinopoisk.services.films_caching import FilmCaching


def cache_film(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        film_caching = FilmCaching()
        cached_film = film_caching.get_film(kwargs['film_id'])
        if cached_film:
            return cached_film
        film = func(*args, **kwargs)
        film_caching.cache_film(film)
        return film
    return wrapper_func

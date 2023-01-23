import orjson

from kinopoisk.clients.redis import RedisClient
from kinopoisk.models.film import Film


class FilmCaching:
    ALL_FILMS_KEY = "all_films"

    def __init__(self):
        self._redis = RedisClient()

    def cache_film(self, film: Film) -> None:
        self._redis.set_cache(str(film.id), film.json())

    def get_film(self, film_id: int) -> Film | None:
        film = self._redis.get_cache(str(film_id))
        if not film:
            return
        return Film.parse_raw(film)

    def set_films(self, films: list[Film]) -> None:
        films = orjson.dumps([film.json() for film in films])
        self._redis.set_cache(self.ALL_FILMS_KEY, films)

    def get_films(self) -> list[Film] | None:
        films = self._redis.get_cache(self.ALL_FILMS_KEY)
        if not films:
            return
        films = [Film.parse_raw(film) for film in orjson.loads(films)]
        return films

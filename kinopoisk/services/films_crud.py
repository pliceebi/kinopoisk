from typing import Union

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_session
from kinopoisk.models.film import Film, FilmCreate, FilmPatch, FilmUpdate

from kinopoisk.exceptions import FilmNotFoundError


class FilmService:

    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def get_film(self, film_id: int) -> Film:
        film = self._session.get(Film, film_id)
        if not film:
            raise FilmNotFoundError()
        return film

    def create_film(self, film: Union[FilmCreate, FilmUpdate]) -> Film:
        film_db = Film.from_orm(film)
        self._session.add(film_db)
        self._session.commit()
        self._session.refresh(film_db)
        return film_db

    def get_films(self) -> list[Film]:
        return self._session.query(Film).all()

    def delete_film(self, film_id: int) -> None:
        film = self.get_film(film_id)
        self._session.delete(film)
        self._session.commit()

    def patch_film(self, film_id: int, film: FilmPatch) -> Film:
        db_film = self.get_film(film_id)
        film_data = film.dict(exclude_unset=True)
        for key, value in film_data.items():
            setattr(db_film, key, value)
        self._session.add(db_film)
        self._session.commit()
        self._session.refresh(db_film)
        return db_film

    def update_film(self, film_id: int, film: FilmUpdate) -> Film:
        try:
            db_film = self.get_film(film_id)
        except FilmNotFoundError:
            return self.create_film(film)
        else:
            film_data = film.dict()
            for key, value in film_data.items():
                setattr(db_film, key, value)
            self._session.add(db_film)
            self._session.commit()
            self._session.refresh(db_film)
            return db_film

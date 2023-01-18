from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from kinopoisk.models.film import FilmRead, FilmPatch, FilmCreate, FilmUpdate
from kinopoisk.services.films import FilmService
from kinopoisk.exceptions import FilmNotFoundError

router = APIRouter(
    prefix='/films',
    tags=['Films'],
)


@router.post('/', response_model=FilmRead)
def create_film(film: FilmCreate, film_service: FilmService = Depends()):
    return film_service.create_film(film)


@router.get('/{film_id}', response_model=FilmRead)
def get_film(film_id: int, film_service: FilmService = Depends()):
    try:
        film = film_service.get_film(film_id)
    except FilmNotFoundError:
        raise HTTPException(status_code=404, detail="Film not found")
    else:
        return film


@router.get('/', response_model=list[FilmRead])
def get_films(film_service: FilmService = Depends()):
    return film_service.get_films()


@router.delete('/{film_id}')
def delete_film(film_id: int, film_service: FilmService = Depends()):
    try:
        film_service.delete_film(film_id)
    except FilmNotFoundError:
        raise HTTPException(status_code=404, detail="Film not found")
    else:
        return {"ok": True}


@router.patch('/{film_id}', response_model=FilmRead)
def patch_film(film_id: int, film: FilmPatch, film_service: FilmService = Depends()):
    try:
        film = film_service.patch_film(film_id, film)
    except FilmNotFoundError:
        raise HTTPException(status_code=404, detail="Film not found")
    else:
        return film


@router.put('/{film_id}', response_model=FilmRead)
def update_film(film_id: int, film: FilmUpdate, film_service: FilmService = Depends()):
    return film_service.update_film(film_id, film)

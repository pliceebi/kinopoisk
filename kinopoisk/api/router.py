from fastapi import APIRouter

from kinopoisk.api.endpoints.films import router as film_router
from kinopoisk.api.endpoints.smoke import router as smoke_router


api_router = APIRouter()
api_router.include_router(film_router)
api_router.include_router(smoke_router)

from fastapi import FastAPI
from sqlmodel import SQLModel

from kinopoisk.api.router import api_router
from database import engine


SQLModel.metadata.create_all(engine)

app = FastAPI()
app.include_router(api_router)

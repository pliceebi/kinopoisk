from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class FilmBase(SQLModel):
    title: str
    description: str
    created_at: datetime = Field(default=datetime.now())
    rating: float


class Film(FilmBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class FilmCreate(FilmBase):
    pass


class FilmRead(FilmBase):
    id: int


class FilmPatch(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None


class FilmUpdate(FilmBase):
    pass

from pydantic import BaseModel, Field

from app.schemas.common import DBModel


class ItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str | None = None


class ItemRead(DBModel):
    id: int
    title: str
    description: str | None
    owner_id: int

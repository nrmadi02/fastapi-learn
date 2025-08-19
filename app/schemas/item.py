from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    title: str | None = None


class ItemInDBBase(BaseModel):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Item(ItemInDBBase):
    title: str
    description: str | None = None


class ItemInDB(ItemInDBBase):
    pass

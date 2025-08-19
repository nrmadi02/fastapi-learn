from __future__ import annotations

from pydantic import BaseModel, EmailStr

from app.schemas.item import Item


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: EmailStr | None = None
    password: str | None = None


class UserInDBBase(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class User(UserInDBBase):
    items: list[Item] = []


class UserInDB(UserInDBBase):
    password: str

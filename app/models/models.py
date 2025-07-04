from typing import List

from pydantic import BaseModel, EmailStr, HttpUrl
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    role: str
    status: str
    email: EmailStr
    avatar: str


class UserCreate(BaseModel):
    id: int | None = None
    name: str
    role: str
    status: str
    email: EmailStr
    avatar: HttpUrl


class UserPatch(BaseModel):
    name: str | None = None
    role: str | None = None
    status: str | None = None
    email: EmailStr | None = None
    avatar: HttpUrl | None = None


class Status(BaseModel):
    database: bool

from typing import List

from pydantic import BaseModel, EmailStr

class UserResp(BaseModel):
    name: str
    job: str
    id: int
    createdAt: str


class UserPayload(BaseModel):
    name: str
    role: str
    status: str
    email: EmailStr


class UserPatchResp(BaseModel):
    name: str
    role: str
    status: str
    email: EmailStr
    updatedAt: str


class User(BaseModel):
    id: int
    name: str
    role: str
    status: str
    email: EmailStr


class UserList(BaseModel):
    items: List[User]


class Status(BaseModel):
    users: bool

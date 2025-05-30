from typing import List

from pydantic import BaseModel

class UserResp(BaseModel):
    name: str
    job: str
    id: int
    createdAt: str


class UserRespList(BaseModel):
    users: List[UserResp]


class UserPayload(BaseModel):
    name: str
    job: str


class UserPatchResp(BaseModel):
    name: str
    job: str
    updatedAt: str

from typing import Iterable

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT, \
    HTTP_422_UNPROCESSABLE_ENTITY

from app.models.models import User, UserCreate, UserPatch

from app.database import users

router = APIRouter(prefix="/api/users")

@router.get("/{id_}", status_code=HTTP_200_OK)
def get_user(id_: int) -> User:
    user = users.get_user(id_)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", status_code=HTTP_201_CREATED)
async def create_user(user: User) -> User:
    try:
        UserCreate.model_validate(user.model_dump())
    except ValidationError as e:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    return users.add_user(user)


@router.delete("/{id_}", status_code=HTTP_204_NO_CONTENT)
def delete_user(id_: int):
    if id_ < 1:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Invalid ID")
    users.remove_user(id_)
    return {"message": "User deleted"}


@router.get("/", status_code=HTTP_200_OK)
def get_users() -> Iterable[User]:
    return users.get_users()


@router.patch("/{id_}", status_code=HTTP_200_OK)
def update_user(id_: int, user: User) -> User:
    if id_ < 1:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Invalid ID")
    UserPatch.model_validate(user.model_dump())
    return users.update_user(user, id_)
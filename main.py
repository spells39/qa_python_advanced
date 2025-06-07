import json
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi_pagination import Page, paginate, add_pagination, Params
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK
from utils.helpers import check_user
from models import UserPayload, UserResp, UserPatchResp, User, Status

app = FastAPI()

users_db: List[UserResp] = None

users: List[User] = None

with open("utils/users.json") as u:
    users = [User(**user) for user in json.load(u)]


@app.get("/api/check_status", status_code=HTTP_200_OK)
def check_status() -> Status:
    return Status(users=bool(users))


@app.get("/api/get_user_by_id/{id_}", status_code=HTTP_200_OK)
def get_user(id_: int) -> User:
    for user in users:
        if user.id == id_:
            return user
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Unknown user")


@app.post("/api/users", response_model=User, status_code=HTTP_201_CREATED)
async def create_user(user: UserPayload):
    new_id = max([user_.id for user_ in users], default=0) + 1
    new_user = User(id=new_id, name=user.name, role=user.role, status=user.status, email=user.email)
    users.append(new_user)
    return new_user


@app.delete("/api/users/{id_}", status_code=HTTP_204_NO_CONTENT)
def delete_user(id_: int):
    global users
    if check_user(id_, users):
        users = [user for user in users if user.id != id_]
        return None
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Unknown user")


@app.get("/api/get_users", response_model=Page[User])
def get_users(page = 1, page_size = len(users)) -> list[User]:
    return paginate(users, params=Params(page=page, size=page_size))


@app.patch("/api/update_user/{id_}", response_model=UserPatchResp)
def update_user(id_: int, user_p: UserPayload):
    global users
    if check_user(id_, users):
        for user in users:
            if user.id == id_:
                user.name = user_p.name
                user.role = user_p.role
                user.status = user_p.status
                user.email = user_p.email
                print(users)
                return UserPatchResp(name=user.name, role=user.role, status=user.status,
                                     email=user.email, updatedAt=str(datetime.utcnow()))
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Unknown user")


add_pagination(app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

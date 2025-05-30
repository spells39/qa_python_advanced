from datetime import datetime
from typing import List

from fastapi import FastAPI, Request, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK
from constants import unknown_users
from helpers import check_user
from models import UserPayload, UserResp, UserRespList, UserPatchResp

app = FastAPI()

users_db: List[UserResp] = []

@app.get("/users/{id_}")
def get_user(id_: int):
    for user in unknown_users:
        if user['id'] == id_:
            return user
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Unknown user")


@app.post("/users", response_model=UserResp, status_code=HTTP_201_CREATED)
async def create_user(user: UserPayload):
    new_id = max([u.id for u in users_db], default=0) + 1
    new_user = UserResp(id=new_id, name=user.name, job=user.job, createdAt=str(datetime.utcnow()))
    users_db.append(new_user)
    return new_user


@app.delete("/users/{id_}", status_code=HTTP_204_NO_CONTENT)
def delete_user(id_: int):
    global users_db
    if check_user(id_, users_db):
        users_db = [user for user in users_db if user.id != id_]
        return None
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Unknown user")


@app.get("/get_users_db", response_model=UserRespList)
def get_users_db():
    return UserRespList(users=users_db)


@app.patch("/users/{id_}", response_model=UserPatchResp)
def update_user(id_: int, user_p: UserPayload):
    global users_db
    if check_user(id_, users_db):
        for user in users_db:
            if user.id == id_:
                user.name = user_p.name
                user.job = user_p.job
                print(users_db)
                return UserPatchResp(name=user.name, job=user.job, updatedAt=str(datetime.utcnow()))
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Unknown user")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

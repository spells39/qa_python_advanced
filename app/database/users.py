from typing import Iterable

from fastapi import HTTPException
from sqlmodel import Session, select

from .engine import engine
from ..models.models import User


def get_user(user_id: int) -> User | None:
    with Session(engine) as session:
        return session.get(User, user_id)

def get_users() -> Iterable[User]:
    with Session(engine) as session:
        statement = select(User)
        return session.exec(statement).all()

def add_user(user: User) -> User:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def remove_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()

def update_user(user: User, user_id: int) -> User:
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = user.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            if value:
                setattr(db_user, key, value)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

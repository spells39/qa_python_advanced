import os

from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlmodel import create_engine, SQLModel, text

engine = create_engine(os.getenv("DATABASE_ENGINE"), pool_size=int(os.getenv("DATABASE_POOL_SIZE", 10)))

def create_db_tables():
    SQLModel.metadata.create_all(engine)


def check_db() -> bool:
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(e)
        return False


def drop_db_tables():
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        if table_name.startswith("user"):
            SQLModel.metadata.tables[table_name].drop(engine)
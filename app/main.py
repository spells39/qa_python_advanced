import logging
from contextlib import asynccontextmanager

import dotenv
import uvicorn

dotenv.load_dotenv()

from fastapi import FastAPI
from app.routers import status, users
from app.database.engine import create_db_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.warning("On startup")
    create_db_tables()
    yield

    logging.warning("On shutdown")


app = FastAPI(lifespan=lifespan)
app.include_router(status.router)
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

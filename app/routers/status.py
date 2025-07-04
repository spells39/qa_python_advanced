from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from app.database.engine import check_db
from app.models.models import Status


router = APIRouter()

@router.get("/api/check_status", status_code=HTTP_200_OK)
def check_status() -> Status:
    return Status(database=check_db())
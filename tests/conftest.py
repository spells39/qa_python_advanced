import os
from pathlib import Path

import dotenv
import pytest
import json
import requests
from starlette.status import HTTP_200_OK


@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()

@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL")

@pytest.fixture(scope="session", autouse=True)
def cleanup_after_tests():
    dotenv.load_dotenv()
    from app.database.engine import drop_db_tables, create_db_tables
    drop_db_tables()
    create_db_tables()
    yield

@pytest.fixture(scope="module")
def fill_db(app_url):
    path = Path(__file__).parent.parent / "utils" / "users.json"
    with open(path) as f:
        users = json.load(f)
    api_users = []
    for user in users:
        resp = requests.post(url=f"{app_url}/api/users/", json=user)
        api_users.append(resp.json())

    yield api_users

    for user in api_users:
        resp = requests.delete(url=f"{app_url}/api/users/{user['id']}")

@pytest.fixture
def users_from_db(app_url):

    def get_users():
        resp = requests.get(url=f"{app_url}/api/users/")
        assert resp.status_code == HTTP_200_OK
        return resp.json()

    return get_users

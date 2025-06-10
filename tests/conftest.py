import os
from pathlib import Path

import dotenv
import pytest
import json

from models import User


@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()

@pytest.fixture
def app_url():
    return os.getenv("APP_URL")

@pytest.fixture
def users():
    users = Path(__file__).parent.parent / "utils" / "users.json"
    with open(users, "r") as f:
        users = [User(**us) for us in json.load(f)]
        return users

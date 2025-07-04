import os
import time

import dotenv
import pytest

from config import Server
from utils.base_session import BaseSession


@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL")


def pytest_addoption(parser):
    parser.addoption("--env", default="dev")

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope='session')
def servicein(env):
    print(f"Передаём в Server: {env}")
    time.sleep(5)
    with BaseSession(base_url=Server(env).service) as session:
        yield session

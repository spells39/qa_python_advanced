import logging
import os
import time

import dotenv

dotenv.load_dotenv()

import pytest

from config import Server
from utils.base_session import BaseSession


@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL")


def pytest_addoption(parser):
    parser.addoption("--env", default="dev")


@pytest.fixture(scope="session")
def env(request):
    envt = request.config.getoption("--env", default="dev")
    logging.info(f"Using env: {envt}")
    return envt


@pytest.fixture(scope='session')
def servicein(env):
    print(f"Передаём в Server: {env}")
    time.sleep(5)
    with BaseSession(base_url=Server(env).service) as session:
        yield session

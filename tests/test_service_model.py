import logging

import pytest
import json
import dotenv
from pathlib import Path

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_405_METHOD_NOT_ALLOWED
)

from app.database.engine import check_db
from app.models.models import User, UserCreate, UserPatch
from app.models.service_model import ServiceModel
from utils.constants import users_for_create, updated_users, user_ids, id_with_status, invalid_data


@pytest.fixture(scope="session", autouse=True)
def cleanup_after_tests():
    dotenv.load_dotenv()
    from app.database.engine import drop_db_tables, create_db_tables
    if check_db():
        drop_db_tables()
        create_db_tables()
    yield


@pytest.fixture(scope="module")
def fill_db(env):
    path = Path(__file__).parent.parent / "utils" / "users.json"
    with open(path) as f:
        users = json.load(f)
    api_users = []
    for user in users:
        resp = ServiceModel(env).create_user(user)
        api_users.append(resp.json())

    yield api_users

    for user in api_users:
        resp = ServiceModel(env).delete_user(user["id"])


@pytest.fixture
def users_from_db(env):

    def get_users():
        resp = ServiceModel(env).get_users()
        assert resp.status_code == HTTP_200_OK
        return resp.json()

    return get_users



class TestUsers:
    @pytest.mark.parametrize('user', users_for_create)
    def test_create_user(self, user, env):
        payload = UserCreate(**user).model_dump(mode="json")
        resp = ServiceModel(env).create_user(payload)
        resp_data = resp.json()

        assert resp.status_code == HTTP_201_CREATED
        assert payload['name'] == resp_data['name']
        assert payload['role'] == resp_data['role']

    @pytest.mark.parametrize('user', invalid_data)
    def test_create_user_invalid_data(self, user, env):
        resp = ServiceModel(env).create_user(user)
        assert resp.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize('user_id, expected_code', id_with_status)
    def test_get_user(self, env, user_id, expected_code):
        resp = ServiceModel(env).get_user(user_id)
        assert resp.status_code == expected_code

    @pytest.mark.parametrize('user_id', user_ids['exist'])
    def test_delete_existed_user(self, user_id, env):
        logging.info(f"Using env: {env}")
        resp = ServiceModel(env).delete_user(user_id)
        assert resp.status_code == HTTP_204_NO_CONTENT

    @pytest.mark.parametrize('user_id', user_ids['not_exist'])
    def test_delete_not_existed_user(self, user_id, env):
        resp = ServiceModel(env).delete_user(user_id)
        assert resp.status_code == HTTP_404_NOT_FOUND

    def test_delete_invalid_method(self, env):
        url = ServiceModel(env).session.base_url + f"users/{user_ids['exist'][0]}"
        resp = env.session.request("POST", url)
        assert resp.status_code == HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.parametrize('user_id, user_up', updated_users)
    def test_update_existed_user(self, user_id, user_up, env):
        payload = UserPatch(**user_up).model_dump(mode="json")
        resp = ServiceModel(env).update_user(user_id, payload)
        assert resp.status_code == HTTP_200_OK
        resp_data = resp.json()
        for field, expected_value in user_up.items():
            if expected_value:
                assert resp_data.get(field) == expected_value

    @pytest.mark.usefixtures("fill_db")
    def test_get_all_users(self, env):
        resp = ServiceModel(env).get_users()
        assert resp.status_code == HTTP_200_OK
        assert len(resp.json()) == 15


class TestSmoke:
    def test_check_status(self, env):
        resp = ServiceModel(env).check_status()
        assert resp.status_code == HTTP_200_OK

    def test_check_status_users(self, env):
        resp = ServiceModel(env).check_status()
        assert resp.status_code == HTTP_200_OK
        assert resp.json()["database"] is True
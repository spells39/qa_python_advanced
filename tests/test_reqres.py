import requests
import pytest
import dotenv
from pathlib import Path
import json

from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_422_UNPROCESSABLE_ENTITY, \
    HTTP_405_METHOD_NOT_ALLOWED

from app.database.engine import check_db
from app.models.models import User, UserCreate, UserPatch
from utils.constants import users_for_create, updated_users, user_ids, id_with_status, invalid_data


@pytest.fixture(scope="class", autouse=True)
def cleanup_after_tests():
    dotenv.load_dotenv()
    from app.database.engine import drop_db_tables, create_db_tables
    if check_db():
        drop_db_tables()
        create_db_tables()
    yield
    if check_db():
        drop_db_tables()
        create_db_tables()

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


class TestUser:
    @pytest.mark.parametrize('user', users_for_create)
    def test_create_user(self, user, app_url, users_from_db):
        payload = UserCreate(**user).model_dump(mode="json")
        resp = requests.post(url=f"{app_url}/api/users/", json=payload)
        resp_from_json = User.model_validate(resp.json())
        assert resp.status_code == 201, "Error, user wasn't created"
        assert payload['name'] == resp_from_json.name and payload['role'] == resp_from_json.role
        users_from_db = users_from_db()
        assert next((u for u in users_from_db if u['id'] == resp_from_json.id), None)

    @pytest.mark.parametrize('user', invalid_data)
    def test_create_user_invalid_data(self, user, app_url):
        resp = requests.post(url=f"{app_url}/api/users/", json=user)
        assert resp.status_code == HTTP_422_UNPROCESSABLE_ENTITY, "Waiting validation error"

    @pytest.mark.parametrize('user_id, expected_code', id_with_status)
    def test_get_user(self, app_url, user_id, expected_code):
        resp = requests.get(url=f"{app_url}/api/users/{user_id}")
        assert resp.status_code == expected_code

    @pytest.mark.parametrize('user_id', user_ids['exist'])
    def test_delete_existed_user(self, user_id, users_from_db, app_url):
        resp = requests.delete(url=f"{app_url}/api/users/{user_id}")
        assert resp.status_code == HTTP_204_NO_CONTENT
        users_after_delete = users_from_db()
        assert not any(user_id == user['id'] for user in users_after_delete), "Error, deletion wasn't successful"

    @pytest.mark.parametrize('user_id', user_ids['not_exist'])
    def test_delete_not_existed_user(self, user_id, app_url):
        resp = requests.delete(url=f"{app_url}/api/users/{user_id}")
        assert resp.status_code == HTTP_404_NOT_FOUND

    def test_delete_invalid_method(self, app_url):
        resp = requests.post(url=f"{app_url}/api/users/{user_ids['exist'][0]}")
        assert resp.status_code == HTTP_405_METHOD_NOT_ALLOWED, "Waiting error 405"

    @pytest.mark.parametrize('user_id, user_up', updated_users)
    def test_update_existed_user(self, user_id, user_up, users_from_db, app_url):
        payload = UserPatch(**user_up).model_dump(mode="json")
        resp = requests.patch(url=f"{app_url}/api/users/{user_id}", json=payload)
        assert resp.status_code == HTTP_200_OK
        User.model_validate(resp.json())
        resp_json = resp.json()
        for field, expected_value in user_up.items():
            if expected_value:
                assert resp_json.get(field) == expected_value
        user_from_db = next((user for user in users_from_db() if user['id'] == user_id), None)
        assert user_from_db
        for field, expected_value in user_up.items():
            if expected_value:
                assert user_from_db.get(field) == expected_value

    @pytest.mark.usefixtures("fill_db")
    def test_get_all_users(self, app_url):
        resp = requests.get(url=f"{app_url}/api/users")
        assert resp.status_code == HTTP_200_OK
        resp_json = resp.json()
        assert len(resp_json) == 15

    @pytest.mark.parametrize('user_id', user_ids['not_exist'])
    def test_update_not_existed_user(self, user_id, app_url):
        resp = requests.patch(url=f"{app_url}/api/users/{user_id}", json=UserPatch().model_dump())
        assert resp.status_code == HTTP_404_NOT_FOUND

    def test_user_lifecycle(self, users_from_db, app_url):
        new_user = {
            "name": "Test User",
            "role": "Tester",
            "status": "active",
            "email": "test@example.com",
            "avatar": "https://example.com/avatar.jpg"
        }
        create_resp = requests.post(url=f"{app_url}/api/users/", json=new_user)
        assert create_resp.status_code == 201
        user_id = create_resp.json()["id"]

        get_resp = requests.get(url=f"{app_url}/api/users/{user_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["name"] == new_user["name"]

        update_data = {"name": "Updated Name"}
        patch_resp = requests.patch(url=f"{app_url}/api/users/{user_id}", json=update_data)
        assert patch_resp.status_code == 200
        assert patch_resp.json()["name"] == update_data["name"]
        user_from_db = next((user for user in users_from_db() if user["id"] == user_id), None)
        assert user_from_db
        assert user_from_db["name"] == update_data["name"]

        delete_resp = requests.delete(url=f"{app_url}/api/users/{user_id}")
        assert delete_resp.status_code == 204
        user_from_db = next((user for user in users_from_db() if user["id"] == user_id), None)
        assert not user_from_db

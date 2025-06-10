from pathlib import Path

import requests
import pytest
import json

from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from models import UserPayload, UserPatchResp, User, UserList
from utils.constants import local_url, headers, users_for_create, updated_users, delete_ids, id_with_status, \
    data_for_test_pagination
from utils.helpers import check_user

#users = Path(__file__).parent.parent / "utils" / "users.json"
#with open(users, "r") as f:
#    users = [User(**us) for us in json.load(f)]

@pytest.mark.parametrize('page_size', [2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_pagination_diff_pages(app_url, page_size, users):
    page_count = len(users) // page_size if len(users) % page_size == 0 else (len(users) // page_size) + 1
    for page in range(page_count):
        resp = requests.get(url=f"{app_url}/api/get_users", params={"page": page + 1, "page_size": page_size})
        assert resp.status_code == HTTP_200_OK
        assert resp.json()['page'] == page + 1
        assert resp.json()['pages'] == page_count
        assert resp.json()['size'] == page_size

def test_pagination_all_users(app_url, users):
    u = users
    resp = requests.get(url=f"{app_url}/api/get_users", params={"page": 1, "page_size": len(users)})
    assert resp.status_code == HTTP_200_OK
    assert resp.json()['pages'] == 1
    assert resp.json()['size'] == len(users)
    assert resp.json()['total'] == len(users)

def test_pagination_diff_pages_diff_data(app_url, users):
    size_1 = len(users) // 2
    size_2 = len(users) - size_1
    resp_1 = requests.get(url=f"{app_url}/api/get_users", params={"page": 1, "page_size": size_1})
    assert resp_1.status_code == HTTP_200_OK
    assert resp_1.json()['size'] == size_1
    resp_2 = requests.get(url=f"{app_url}/api/get_users", params={"page": 2, "page_size": size_2})
    assert resp_2.status_code == HTTP_200_OK
    assert resp_2.json()['size'] == size_2
    resp_1_users = [User(**us) for us in resp_1.json()['items']]
    resp_2_users = [User(**us) for us in resp_2.json()['items']]
    assert resp_1_users != resp_2_users

@pytest.mark.parametrize('page_id, page_size, expected_ids', data_for_test_pagination)
def test_pagination(app_url, page_id, page_size, expected_ids):
    resp = requests.get(url=f"{app_url}/api/get_users", params={"page": page_id, "page_size": page_size})
    assert resp.status_code == HTTP_200_OK
    resp_ids = [User(**us).id for us in resp.json()['items']]
    assert set(expected_ids) == set(resp_ids), "Incorrect pagination"


@pytest.mark.parametrize('user_id, expected_code', id_with_status)
def test_get_user(app_url, user_id, expected_code):
    resp = requests.get(url=f"{app_url}/api/get_user_by_id/{user_id}", headers=headers)
    assert resp.status_code == expected_code

@pytest.mark.parametrize('user', users_for_create)
def test_create_user(user):
    payload = UserPayload(name=user['name'],
                          role=user['role'],
                          status=user['status'],
                          email=user['email'])
    resp = requests.post(url=f"{local_url}/api/users", headers=headers, json=payload.dict())
    resp_from_json = User.parse_raw(resp.text)
    assert resp.status_code == 201, "Error, user wasn't created"
    assert payload.name == resp_from_json.name and payload.role == resp_from_json.role

@pytest.mark.parametrize('user_id', delete_ids['exist'])
def test_delete_existed_users(user_id):
    users_db_resp = requests.get(url=f"{local_url}/api/get_users")
    users_db = UserList.parse_raw(users_db_resp.text).items
    resp = requests.delete(url=f"{local_url}/api/users/{user_id}", headers=headers)
    users_db_del_resp = requests.get(url=f"{local_url}/api/get_users")
    users_db_del = UserList.parse_raw(users_db_del_resp.text).items
    assert not any(user_id == user.id for user in users_db_del), "Error, deletion wasn't successful"

@pytest.mark.parametrize('user_id', delete_ids['not_exist'])
def test_delete_not_existed_users(user_id):
    resp = requests.delete(url=f"{local_url}/api/users/{user_id}", headers=headers)
    assert resp.status_code == HTTP_404_NOT_FOUND

@pytest.mark.parametrize('user_id, user_up', updated_users)
def test_update_user(user_id, user_up):
    users_db_resp = requests.get(url=f"{local_url}/api/get_users")
    users_db = UserList.parse_raw(users_db_resp.text).items
    payload = UserPayload(name=user_up['name'], role=user_up['role'], status=user_up['status'],
                          email=user_up['email']).dict()
    resp = requests.patch(url=f"{local_url}/api/update_user/{user_id}", headers=headers, json=payload)
    if check_user(user_id, users_db):
        users_db_up_resp = requests.get(url=f"{local_url}/api/get_users")
        users_db_up = UserList.parse_raw(users_db_up_resp.text).items
        assert resp.status_code == 200
        resp_parsed = UserPatchResp.parse_raw(resp.text)
        assert resp_parsed.name == user_up['name'] and resp_parsed.role == user_up['role']
        assert (any(user_up['name'] == user.name for user in users_db_up) and
                any(user_up['role'] == user.role for user in users_db_up)), "Error, update wasn't successful"
    else:
        assert resp.status_code == 404

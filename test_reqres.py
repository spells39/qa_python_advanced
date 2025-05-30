import requests
import pytest

from models import UserPayload, UserResp, UserRespList, UserPatchResp
from constants import local_url, headers, users_for_create, updated_users, delete_ids, id_with_status
from helpers import check_user

@pytest.mark.parametrize('user_id, expected_code', id_with_status)
def test_get_user(user_id, expected_code):
    resp = requests.get(url=f"{local_url}/users/{user_id}", headers=headers)
    assert resp.status_code == expected_code

@pytest.mark.parametrize('user', users_for_create)
def test_create_user(user):
    payload = UserPayload(name=user['name'],
                          job=user['role'])
    resp = requests.post(url=f"{local_url}/users", headers=headers, json=payload.dict())
    resp_from_json = UserResp.parse_raw(resp.text)
    assert resp.status_code == 201
    assert payload.name == resp_from_json.name and payload.job == resp_from_json.job

@pytest.mark.parametrize('user_id', delete_ids)
def test_delete_users(user_id):
    users_db_resp = requests.get(url=f"{local_url}/get_users_db")
    users_db = UserRespList.parse_raw(users_db_resp.text).users
    resp = requests.delete(url=f"{local_url}/users/{user_id}", headers=headers)
    if check_user(user_id, users_db):
        users_db_del_resp = requests.get(url=f"{local_url}/get_users_db")
        users_db_del = UserRespList.parse_raw(users_db_del_resp.text).users
        assert not any(user_id == user.id for user in users_db_del), "Error, deletion wasn't successful"
    else:
        assert resp.status_code == 404

@pytest.mark.parametrize('user_id, user_up', updated_users)
def test_update_user(user_id, user_up):
    users_db_resp = requests.get(url=f"{local_url}/get_users_db")
    users_db = UserRespList.parse_raw(users_db_resp.text).users
    payload = UserPayload(name=user_up['name'], job=user_up['job']).dict()
    resp = requests.patch(url=f"{local_url}/users/{user_id}", headers=headers, json=payload)
    if check_user(user_id, users_db):
        users_db_up_resp = requests.get(url=f"{local_url}/get_users_db")
        users_db_up = UserRespList.parse_raw(users_db_up_resp.text).users
        assert resp.status_code == 200
        resp_parsed = UserPatchResp.parse_raw(resp.text)
        assert resp_parsed.name == user_up['name'] and resp_parsed.job == user_up['job']
        assert (any(user_up['name'] == user.name for user in users_db_up) and
                any(user_up['job'] == user.job for user in users_db_up)), "Error, update wasn't successful"
    else:
        assert resp.status_code == 404

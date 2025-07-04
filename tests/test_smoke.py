import requests
from starlette.status import HTTP_200_OK

from app.models.models import Status

def test_check_status(app_url):
    resp = requests.get(f"{app_url}/api/check_status")
    assert resp.status_code == HTTP_200_OK

def test_check_status_users(app_url):
    resp = requests.get(f"{app_url}/api/check_status")
    assert resp.status_code == HTTP_200_OK
    assert Status.parse_raw(resp.text).database

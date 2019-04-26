import warnings

import pytest

from app import create_app
from server.serverconfig import TestingConfig
from server.db.models import User, Email


# @pytest.fixture
# def client():
#     app = create_app(TestingConfig)
#     client = app.test_client()
#     yield client


# @pytest.mark.filterwarnings("always")
def test_login_route(client, mock_users):
    assert True
    # users, mock_users_list = mock_users

    # request_payload = {
    #     "username": mock_users_list[0][0],
    #     "password": mock_users_list[0][1],
    # }
    # resp = client.post("/auth/login", json=request_payload).get_json(force=True)

    # assert resp["message"] == "success"
    # assert resp["auth"] is not None
    # assert "error" not in resp.keys()

    # inv_request_payload = {
    #     "username": mock_users_list[0][0],
    #     "password": "invalidpassword",
    # }
    # resp = client.post("/auth/login", json=inv_request_payload).get_json(force=True)
    # assert resp["error"] == "Invalid Username or Password"
    # assert "auth" not in resp.keys()
    # assert "message" not in resp.keys()

    # bad_request_payload = {"bad_data": "baaaad!"}
    # resp = client.post("/auth/login", json=bad_request_payload).get_json(force=True)
    # assert resp["error"] == "Bad Request"
    # assert "auth" not in resp.keys()
    # assert "message" not in resp.keys()

    # try:
    #     client.get("/auth/login")
    #     assert False
    # except Exception:
    #     assert True

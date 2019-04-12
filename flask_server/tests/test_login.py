import pytest

from app import app
from server.serverconfig import TestingConfig
from server.db import db_session
from server.models import User, Email

mock_users_list = [
    ('testuser' + str(i), 'password1234', f'email{i}@email.com') for i in range(10)
]




@pytest.fixture
def client():
    app.config.from_object(TestingConfig)
    client = app.test_client()


    yield client
    db_session.remove()


@pytest.fixture
def mock_users():
    user_list = []
    for u in mock_users_list:
        username, password, email = u
        try:
            current_user = db_session.query(User).filter(
                User.username == username, email == email).one()
            user_list.append(current_user)
        except Exception as e:
            try:
                new_user = User(username, password, email)
            except AssertionError:
                continue
            db_session.add(new_user)
            db_session.commit()
            user_list.append(new_user)
    return user_list


def test_default_route(client):
    res = client.get('/')
    assert b'<h1>hello world</h1>' in res.data


def test_loging_route(client,mock_users):
    request_payload = {
        'username': mock_users_list[0][0], 'password': mock_users_list[0][1]}
    resp = client.post('/auth/login', json=request_payload).get_json(force=True)
    
    assert resp['message'] == 'success'
    assert resp['auth'] is not None
    assert 'error' not in resp.keys()

    inv_request_payload = {
        'username': mock_users_list[0][0], 'password': 'invalidpassword'}
    resp = client.post('/auth/login', json=inv_request_payload).get_json(force=True)
    assert resp['error'] == 'Invalid Username or Password'
    assert 'auth' not in resp.keys()
    assert 'message' not in resp.keys()

    bad_request_payload = {'bad_data':'baaaad!'}
    resp = client.post('/auth/login', json=bad_request_payload).get_json(force=True)
    assert resp['error'] == 'Invalid Request'
    assert 'auth' not in resp.keys()
    assert 'message' not in resp.keys()

    try:
        client.get('/auth/login')
        assert False
    except Exception:
        assert True
    

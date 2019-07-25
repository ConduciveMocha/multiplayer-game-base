import pytest
import jwt
from datetime import datetime, timedelta
from server.auth import UserAuthenticator
from app import create_app
from server.serverconfig import TestingConfig


@pytest.fixture
def with_auth():
    app = create_app(TestingConfig)
    auth = UserAuthenticator()
    auth.init_app(app)
    yield auth, app


"""
    Fixture that generates JWTS:
        0. Valid
        1. Invalid Issuer URL
        2. Invalid Issue Time
        3. Invalid Expiration Time
"""


@pytest.fixture
def make_test_jwts(with_auth):
    auth, app = with_auth

    # Valid JWT
    valid = auth.login_jwt(0)
    # Bad issuer
    invalid_iss = auth.login_jwt(0, iss="http://badurl.com")
    # Issue date in future
    invalid_iat = auth.login_jwt(0, iat=datetime.utcnow() + timedelta(seconds=3600))
    # Token expired
    invalid_exp = auth.login_jwt(0, exp_delta=-25)
    return auth, (valid, invalid_iss, invalid_iat, invalid_exp)


"""
    Tests the login_jwt which returns a JWT for a given user id
"""


def test_login_jwt(make_test_jwts):
    auth, test_jwts = make_test_jwts
    jwt_0 = test_jwts[0]
    payload = jwt.decode(jwt_0, key=auth.JWT_KEY, algorithms=auth.JWT_ALGORITHMS)
    # Correct issuer
    assert payload["iss"] == auth.JWT_ISS
    # Correct id
    assert payload["user_id"] == 0
    # Issued prior to now
    assert datetime.utcfromtimestamp(payload["iat"]) < datetime.utcnow()
    # Has not expired
    assert datetime.utcfromtimestamp(payload["exp"]) > datetime.utcnow()


"""
    Tests verify_jwt which takes a jwt and ensures its valid
"""


def test_verify_jwt(make_test_jwts):
    auth, make_test_jwts = make_test_jwts
    valid, invalid_iss, invalid_iat, invalid_exp = make_test_jwts

    assert auth.verify_jwt(valid, user_id=0)  # Valid token
    assert auth.verify_jwt("", user_id=0) == False  # No token passed
    assert auth.verify_jwt(valid, user_id=5) == False  # Incorrect id
    assert auth.verify_jwt(invalid_iss, user_id=0) == False  # Bad issuer
    assert auth.verify_jwt(invalid_iat, user_id=0) == False  # Bad issue time
    assert auth.verify_jwt(invalid_exp, user_id=0) == False  # Expired


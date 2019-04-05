import pytest
import jwt
from datetime import datetime,timedelta

from server.auth import login_jwt,verify_jwt,JWT_ALGORITHMS,JWT_SECRET, JWT_ISS



"""
    Fixture that generates JWTS:
        0. Valid
        1. Invalid Issuer URL
        2. Invalid Issue Time
        3. Invalid Expiration Time
"""
@pytest.fixture
def make_test_jwts():
    valid = login_jwt(0)                                                        # Valid JWT
    invalid_iss = login_jwt(0,iss='http://badurl.com')                          # Bad issuer
    invalid_iat = login_jwt(0,iat=datetime.utcnow()+timedelta(seconds=3600))    # Issue date in future
    invalid_exp = login_jwt(0,exp_delta=-25)                                    # Token expired
    return (valid,invalid_iss,invalid_iat,invalid_exp)

"""
    Tests the login_jwt which returns a JWT for a given user id
"""
def test_login_jwt(make_test_jwts):
    jwt_0 = make_test_jwts[0]
    payload = jwt.decode(jwt_0,key=JWT_SECRET,algorithms=JWT_ALGORITHMS)

    assert payload['iss'] == JWT_ISS                                      # Correct issuer
    assert payload['user_id'] == 0                                        # Correct id
    assert datetime.utcfromtimestamp(payload['iat']) < datetime.utcnow()  # Issued prior to now
    assert datetime.utcfromtimestamp(payload['exp']) > datetime.utcnow()  # Has not expired

"""
    Tests verify_jwt which takes a jwt and ensures its valid
"""
def test_verify_jwt(make_test_jwts):
    valid, invalid_iss, invalid_iat,invalid_exp = make_test_jwts

    assert verify_jwt(valid, user_id=0)                                   # Valid token
    assert verify_jwt('', user_id=0) == False                             # No token passed
    assert verify_jwt(valid, user_id=5) == False                          # Incorrect id
    assert verify_jwt(invalid_iss, user_id=0)== False                     # Bad issuer
    assert verify_jwt(invalid_iat, user_id=0) == False                    # Bad issue time
    assert verify_jwt(invalid_exp, user_id=0)== False                     # Expired


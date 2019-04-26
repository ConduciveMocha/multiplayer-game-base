import json
import jwt
import base64

from functools import wraps
from datetime import datetime, timedelta

from flask import jsonify, request, g
from server.logging import serverlogger


"""
    Returns a JWT for a giver user id
"""


class UserAuthenticator:
    def __init__(
        self,
        JWT_ISS=None,
        JWT_EXP_DELTA_SECONDS=None,
        JWT_KEY=None,
        JWT_ALGORITHMS=None,
    ):
        self.app = None
        self.JWT_ISS = JWT_ISS
        self.JWT_EXP_DELTA_SECONDS = JWT_EXP_DELTA_SECONDS
        self.JWT_KEY = JWT_KEY
        self.JWT_ALGORITHMS = JWT_ALGORITHMS

    def init_app(self, app):
        self.app = app
        self.JWT_ISS = app.config.get("JWT_ISS")
        self.JWT_EXP_DELTA_SECONDS = app.config.get("JWT_EXP_DELTA_SECONDS")
        self.JWT_KEY = app.config.get("JWT_KEY")
        self.JWT_ALGORITHMS = app.config.get("JWT_ALGORITHMS")

    def login_jwt(self, user_id, iat=None, iss=None, exp_delta=None):

        payload = {
            "iss": iss if iss else self.JWT_ISS,
            "user_id": user_id,
            "iat": iat if iat else datetime.utcnow(),
            "exp": datetime.utcnow()
            + timedelta(
                seconds=(exp_delta if exp_delta else self.JWT_EXP_DELTA_SECONDS)
            ),
        }
        token = jwt.encode(payload, self.JWT_KEY, self.JWT_ALGORITHMS[0])
        return token

    def verify_jwt(self, token, user_id=None, decoded=False):
        if not token:
            serverlogger.info("JWT Error: no token")
            return False
        # Catch errors from jwt decode and KeyError
        try:
            # Decodes if necessary
            payload = (
                token
                if decoded
                else jwt.decode(token, key=self.JWT_KEY, algorithms=self.JWT_ALGORITHMS)
            )

            # Bad Issuer
            if payload["iss"] != self.JWT_ISS:
                serverlogger.info("JWT Error: bad issuer")
                return False

            # Bad Issue Time
            elif datetime.utcfromtimestamp(payload["iat"]) > datetime.utcnow():
                serverlogger.info("JWT Error: bad iat")
                return False

            # Bad User id
            elif user_id is not None and payload["user_id"] != user_id:
                serverlogger.info("JWT Error: bad user_id")
                return False
            else:
                return True

        # jwt.decode failed
        except jwt.DecodeError as e:
            serverlogger.error("JWT Error: decode error")
            serverlogger.debug(e)
            return False
        # Signature invalid
        except jwt.ExpiredSignatureError as e:
            serverlogger.info("JWT Error: expired signature")
            serverlogger.debug(e)
            return False
        # Bad Payload
        except KeyError as e:
            serverlogger.info("JWT Error: bad payload")
            serverlogger.debug(e)
            return False


"""
    Decorator that wraps routes requiring an Auth Token
"""


def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers.get("authorization", None)
            payload = request.get_json()

            if not g.auth.verify_jwt(token, user_id=payload["userId"]):
                return json.dumps({"error": "Token is invalid"}), 400
            else:
                return func(*args, **kwargs)
        except TypeError as e:
            serverlogger.error(e)
            return jsonify(error="Invalid Request"), 400

    return wrapper


def make_thread_hash(members):
    enc = "_".join(map(lambda x: str(x), members.sort()))
    return base64.b64encode(enc.encode("utf-8")).decode("utf-8")


def members_from_thread_hash(thread_id):
    dec = base64.b64decode(thread_id).decode("utf-8")
    dec = dec.split("_")
    members = []
    for i, m in enumerate(dec):
        if i == 0:
            members.append(int(m))
        else:
            members.append(members[-1] + int(m))
    return members

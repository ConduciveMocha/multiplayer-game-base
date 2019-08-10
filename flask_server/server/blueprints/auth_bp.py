import json
import logging
from flask import Blueprint, request, make_response, jsonify, current_app, g

from server.logging import request_log, make_logger
from server.db.models import User
from server.db.user_actions import verify_user
from server.redis_cache.user_cache import set_user_online, set_user_offline, user_online
from server.auth import require_auth
from server.utils.errors import required_or_400


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

auth_logger = make_logger(__name__)
"""
    Login endpoint. Returns a JWT if successful
"""


@auth_bp.route("/login", methods=["POST", "GET"])
@required_or_400(required=["username", "password"])
def login():

    username, password = g.username, g.password
    user = verify_user(username, password)
    if user:
        token = g.auth.login_jwt(user.id)
        set_user_online(user)

        return json.dumps({"message": "success", "auth": token.decode("utf-8")}), 200
    else:
        return json.dumps({"error": "Invalid Username or Password"}), 401


"""
    Logout endpoint
"""
# TODO Write this method
@auth_bp.route("/logout", methods=["POST"])
@request_log(request)
@require_auth
@required_or_400(required="userId", logger=auth_logger)
def logout():

    user_id = g.userId
    if user_online(user_id):
        set_user_offline(user_id)
        auth_logger.info(f"User `{user_id}` successfully logged off")
        return jsonify(message="Success"), 501
    else:
        auth_logger.info(
            f"A valid logoff request was sent by user not found in `user:online`. Id: {user_id}"
        )
        return jsonify(message="Already offline")

    return "logout", 501

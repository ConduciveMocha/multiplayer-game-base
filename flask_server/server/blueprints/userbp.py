import json
from flask import Blueprint, request, jsonify

from server.logging import request_log
from server.db.user_actions import query_user_by_id, query_user_by_username
from server.auth import require_auth
from server.redis_cache.user_cache import get_user, get_online_users

userbp = Blueprint("user", __name__, url_prefix="/user")


@userbp.route("/online")
@require_auth
def request_userlist():
    """Gets mapping of users -> usernames for online users
    """
    return get_online_users()


@userbp.route("/<int:user_id>")
@require_auth
def request_username(user_id):
    """Queries user by ID
    """
    cache_result = get_user(user_id)
    if cache_result:
        return cache_result
    else:
        queried_user = query_user_by_id(user_id)
        if queried_user:
            return jsonify(user={user_id: queried_user.username})
        else:
            return jsonify(user={})


@userbp.route("/<string:username>")
@require_auth
def request_user_id(username):
    """Queries User by username
    """
    # TODO rework redis so that i can efficiently query users by username
    pass

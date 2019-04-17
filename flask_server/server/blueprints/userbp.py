import json
from flask import Blueprint, request, jsonify

from server.loggers.serverlogger import request_log
from server.cachemanager import poolman
from server.auth import require_auth
from server.db import db_session
from server.models import User


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/')
@require_auth
def request_userlist():
    """Gets mapping of users -> usernames for online users
    """
    with poolman as r:
        user_list = {user_id: r.hget(
            f'user:{user_id}', 'username') for user_id in r.sscan_iter('user:online')}
    return jsonify(usersOnline=user_list)


@bp.route('/<int:user_id>')
@require_auth
def request_username(user_id):
    """Queries user by ID
    """
    with poolman as r:
        if r.exists(f'user:{user_id}'):
            return jsonify(user={user_id: r.hget(f'user:{user_id}', 'username')})
        else:
            queried_user = db_session.query(User).filter(
                User.id == user_id).one_or_none()
            if queried_user:
                return jsonify(user={user_id: queried_user.username})
            else:
                return jsonify(error="No user found")


@bp.route('/<string:username>')
def request_user_id(username):
    """Queries User by username
    """
    # TODO rework redis so that i can efficiently query users by username
    pass

import json
from flask import Blueprint, request,make_response

from server.loggers.serverlogger import request_log
from server.db.usersession import UserSession

_user_session = UserSession()

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/')
def request_userlist():
    pass

@bp.route('/<int:user_id>')
def request_username(user_id):
    pass

@bp.route('/<string:username>')
def request_user_id(username):
    pass
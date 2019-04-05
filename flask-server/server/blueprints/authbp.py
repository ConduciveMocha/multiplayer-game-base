import json
from flask import Blueprint,request,make_response

from server.auth import login_jwt, require_auth
from server.loggers.serverlogger import request_log
from server.db.usersession import UserSession

_user_session = UserSession()
bp = Blueprint('auth',__name__,url_prefix='/auth')

"""
    Login endpoint. Returns a JWT if successful
"""
@bp.route('/login', methods=['POST'])
@request_log(request)
def login():

    data = request.get_json()
    if 'username' in data.keys() and 'password' in data.keys():
        user_id = _user_session.check_login(data['username'], data['password'])
        if isinstance(user_id, int):
            token = login_jwt(user_id)


            return json.dumps({'message':'success','auth':token}),200
        else:
            return json.dumps({'error': 'Invalid Username or Password'}), 401
    else:
         raise Exception(f'Username or password not in data.keys(): ({data.keys()})')

"""
    Logout endpoint
"""
#TODO Write this method
@bp.route('/logout',methods=['POST'])
@request_log(request)
def logout():
    return 'logout',501

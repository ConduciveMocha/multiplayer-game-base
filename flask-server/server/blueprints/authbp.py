import json
from flask import Blueprint,request,make_response

from server.auth import login_jwt, require_auth
from server.loggers.serverlogger import request_log
from server.db  import db_session

authbp = Blueprint('auth',__name__,url_prefix='/auth')

"""
    Login endpoint. Returns a JWT if successful
"""
@authbp.route('/login', methods=['POST'])
@request_log(request)
def login():
    payload = request.get_json()
    try:
        username, password = data['username'], data['password']
        user_match = db_session.query(User).filter(User.username==username).one()
        if user_match.check_login(username,password):
            token = login_jwt(user_match.user_id)
            return json.dumps({'message': 'success', 'auth': token}), 200
        else:
            return json.dumps({'error': 'Invalid Username or Password'}), 401   
    except KeyError:
        return json.dumps({'error':'Invalid Request'}), 400
    

"""
    Logout endpoint
"""
#TODO Write this method
@authbp.route('/logout',methods=['POST'])
@request_log(request)
def logout():
    return 'logout',501

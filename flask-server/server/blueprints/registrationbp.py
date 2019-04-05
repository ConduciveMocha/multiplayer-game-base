import json
from flask import Blueprint, request,make_response

from server.loggers.serverlogger import request_log
from server.db.usersession import UserSession

_user_session = UserSession()

bp = Blueprint('register', __name__, url_prefix='/register')


"""
    API endpoint for creating new user. 
"""
@bp.route('/create', methods=['POST'])
@request_log(request)
def create_account():
    try:
        username=  request.form['username']
        password = request.form['password']
        email = request.form['email']
        msg, user_id = _user_session.add_user(username,password,email)
        if user_id is -1: raise ValueError
    except Exception as e:
        return json.dumps({'error':'error creating user'}),409
    return json.dumps({'message':msg,'user_id':user_id}),201




"""
    API endpoint for checking if a username is valid before 
    account creation request is submitted.
"""
@bp.route('/check-availability')
@request_log(request)
def check_availability():

    payload = request.get_json()
    email = payload.get('email', None)
    username = payload.get('username', None)
    response_dict = {}
    if email:
        if _user_session.valid_email(email):
            response_dict['email'] = 'Unavailable' if  _user_session.email_in_use(email) else 'Available'
        else:
            response_dict['email'] = 'Invalid'
    if username:
        if _user_session.valid_username(username):
            response_dict['username'] = 'Unavailable' if _user_session.email_in_use(email) else 'Available'
        else:
            response_dict['username'] = 'Invalid'
    return make_response(json.dumps(response_dict), 200)
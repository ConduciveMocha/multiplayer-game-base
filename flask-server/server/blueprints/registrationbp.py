import json
from flask import Blueprint, request,make_response

from server.models import User, Email
from server.loggers.serverlogger import request_log
from server.db import db_session



registrationbp = Blueprint('register', __name__, url_prefix='/register')


"""
    API endpoint for creating new user. 
"""
@registrationbp.route('/create', methods=['POST'])
@request_log(request)
def create_account():
    try:
        payload = request.get_json()
        username=  payload['username']
        password = payload['password']
        email = payload['email']
    
        new_user = User(username,password,email)

        db_session.add(new_user)
        db_session.commit()

        return json.dumps({'message':'success','user_id':new_user.user_id}),201
    except AssertionError as e:
        return json.dumps({'error':'Invalid username or password'})
    except Exception as e:
        return json.dumps({'error':'error creating user'}),409




"""
    API endpoint for checking if a username is valid before 
    account creation request is submitted.
"""
@registrationbp.route('/check-availability')
def check_availability():

    payload = request.get_json()
    email = payload.get('email', None)
    username = payload.get('username', None)
    
    response_dict = {}
    if email:
        response_dict['email'] = 'Unavailable' if db_session.query(Email).filter(Email.email == email).one_or_none() else 'Available'
    if username:
        response_dict['username'] = 'Unavailable' if db_session.query(User).filter(User.username==username) else 'Available'
        
    return make_response(json.dumps(response_dict), 200)
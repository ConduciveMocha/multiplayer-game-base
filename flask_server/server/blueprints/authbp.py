import json
from flask import Blueprint, request, make_response, jsonify

from server.auth import login_jwt, require_auth
from server.loggers.serverlogger import request_log
from server.db import db_session
from server.models import User
from server.cachemanager import poolman
authbp = Blueprint('auth', __name__, url_prefix='/auth')

"""
    Login endpoint. Returns a JWT if successful
"""
@authbp.route('/login', methods=['POST'])
@request_log(request)
def login():
    try:
        payload = request.get_json()
        username, password = payload['username'], payload['password']
        user_match = db_session.query(User).filter(
            User.username == username).one()
        if user_match.check_login(username, password):

            token = login_jwt(user_match.id)

            with poolman as r:
                # Checks if user is online
                if r.sismember('user:online', user_match.id):
                    return jsonify(error='User logged in somewhere else')
                else:
                    r.sadd('user:online', user_match.id)

                # Checks if user is cached
                if r.exists(f'user:{user_match.id}'):
                    r.hset(f'user:{user_match.id}', 'online', 1)

                # Not cached...
                else:
                    with r.pipeline() as pipe:
                        pipe.hmset(f'user:{user_match.id}', {
                                   'username': user_match.username, 'online': 1})

                        # Sets user:<id>:threads and sends requests to load threads not cached
                        for thread in user_match.message_threads:
                            pipe.zadd(
                                f'user:{user_match.id}:threads', thread.created, thread.id)

                            if not r.exists(f'thread:{thread.id}'):
                                # TODO Dispatch Celery Task -- Load threads
                                pass

                        pipe.execute()

            return json.dumps({'message': 'success', 'auth': token.decode('utf-8')}), 200
        else:
            return json.dumps({'error': 'Invalid Username or Password'}), 401
    except KeyError:
        return json.dumps({'error': 'Invalid Request'}), 400


"""
    Logout endpoint
"""
# TODO Write this method
@authbp.route('/logout', methods=['POST'])
@request_log(request)
def logout():

    return 'logout', 501

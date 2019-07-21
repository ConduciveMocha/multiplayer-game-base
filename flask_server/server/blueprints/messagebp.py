import json
import base64
import time
from flask import Blueprint, request, make_response, jsonify
from flask_socketio import SocketIO, emit, send, Namespace

from server.db import db_session
from server.auth import make_thread_id, members_from_thread_id, require_auth
from server.models import User, Thread
from server.cachemanager import poolman

bp = Blueprint('message', __name__, url_prefix='/message')


def match_users_to_threads(user_list,thread_list):
    for thread in thread_list:
        if all(user in thread.users for user in user_list) \
        and len(user_list) == len(thread.users):
            return thread        
    return None


@bp.route('/requestthread', methods=['POST'])
@require_auth
def request_thread():
    try:
        payload = request.get_json()
        requesting_user_id = payload.get('user', None)
    except AttributeError:
        return jsonify(error="No payload passed"), 400
    
    if not requesting_user_id:
        return jsonify(error='No user id'), 400


    try:
        requesting_user = db_session.query(User).filter(User.id == requesting_user).one_or_none()
        requesting_user_threads = requesting_user.message_threads
    except AttributeError as e:
        return jsonify(error='User was not found'), 400

    thread_members = payload.get('members', [])
    if len(thread_members) == 0:
        return jsonify(error='No thread members passed'), 400


    requested_thread = match_users_to_threads(thread_members, thread_list)

    

@bp.route('/history')
def thread_history():
    try:
        payload = request.get_json()
        thread_id = payload['threadId']
        user_id = payload['userId']
        start = payload['start']

        if user_id not in members_from_thread_id(thread_id):
            return jsonify(error='User does not have access to thread')

        message_dict = {}
        with poolman as r:
            # Thread in redis
            if r.exists(f'thread:{thread_id}'):
                oldest_message_id, oldest_message_time = r.zrange(
                    f'thread:{thread_id}:message', -2, -1, withscores=True)

                # Thread not entirely in redis
                if oldest_message_time > start and oldest_message_id != "THREAD_START":
                    # TODO Dispatch Celery task -- Thread not all in db
                    return jsonify(error='This isnt implemented. messagedb.py ln 97')

                # Thread saved in redis
                else:
                    # ask about this. This whole thing will run super slow
                    message_ids = r.zrangebyscore(
                        f'thread:{thread_id}:messages', start, time.time())
                    for m_id in message_ids:
                        message_dict[m_id] = r.hgetall(f'message:{m_id}')
                    return jsonify(message_dict)

            else:
                # TODO Dispatch celery task -- Thread not in redis
                return jsonify(error='This isnt implemented. messagedb.py ln 110')

    except Exception as e:
        return jsonify(error="Error getting thread history")

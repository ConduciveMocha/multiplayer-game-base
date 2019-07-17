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


@bp.route('/createthread', methods=['POST'])
@require_auth
def create_thread():
    # DB code here
    try:
        payload = request.get_json()
        thread_id = payload.get('id', None)

        # No Thread Id
        if thread_id is None:
            return jsonify(error="Needs thread id")

        # User needs to be a member of the thread
        member_ids = members_from_thread_id(thread_id)
        if int(payload.get('userId', -1)) not in member_ids:
            return jsonify(error="Authentication error")

        with poolman as r:
            if r.exists(f'thread:{thread_id}'):
                return jsonify(message="Thread active")

        # Tries to get thread from db
        thread = db_session.query(Thread).filter(
            Thread.id == thread_id).one_or_none()
        if thread is None:

            if len(member_ids) > 10:
                return jsonify(error="Thread too large")

            members = db_session.query(User).filter(User.id.in_(member_ids))

            if len(members) != len(member_ids):
                return jsonify(error="Invalid threadId")

            thread = Thread(
                members, thread_name=payload.get('threadName', None))
            db_session.add(thread)
            db_session.commit()

    except Exception as e:
        return jsonify(error=str(type(e)))

    # TODO Add lock?
    with poolman.pipe() as pipe:
        time_created = time.time()

        # Sets thread metadata
        pipe.hmset(f'thread:{thread_id}', {'members': ':'.join(
            member_ids), 'created': time_created})

        # Creates a message Zet
        pipe.zadd(f'thread:{thread_id}:messages', time_created, "THREAD_START")

        # Adds thread to user's active threads
        for member_id in member_ids:
            if pipe.exists(f'user:{member_id}'):
                pipe.zadd(f'user:{member_id}:threads', time_created, thread_id)

        pipe.execute()

    # TODO WEBSOCKET CREATE THREAD CODE HERE


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

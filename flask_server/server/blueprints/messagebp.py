import json
import base64

from flask import Blueprint, request, make_response, jsonify
from flask_socketio import SocketIO, emit, send, Namespace

from server.db import db_session
from server.auth import make_thread_id, members_from_thread_id, require_auth
from server.models import User, Thread, Message

bp = Blueprint('message', __name__, url_prefix='/message')


@bp.route('/createthread', methods=['POST'])
@require_auth
def create_thread():
    # DB code here
    try:
        payload = request.get_json()
        thread_id = payload.get('threadId', None)

        # No Thread Id
        if thread_id is None:
            return jsonify(error="Needs thread id")

        # User needs to be a member of the thread
        member_ids = members_from_thread_id(thread_id)
        if payload.get('user_id', '-1') not in member_ids:
            return jsonify(error="Authentication error")

        # TODO CHECK REDIS IF THREAD IS ACTIVE HERE

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

    # TODO REDIS CREATE THREAD CODE HERE
    # TODO WEBSOCKET CREATE THREAD CODE HERE


@bp.route('/history')
def thread_history():
    pass

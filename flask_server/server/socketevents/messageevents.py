import json
import logging


from flask import session, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect, send
from redis.exceptions import DataError


from server.auth import require_auth
from server.db.user_actions import query_user_by_id
from server.db.models import Thread
from server.redis_cache.user_cache import (
    set_user_online,
    set_user_offline,
    user_from_sid,
    user_from_cache,
)
from server.redis_cache.message_cache import get_message_by_id, create_message_dict,create_message,check_if_thread_exists, create_thread,get_next_id
from server.logging import make_logger

try:
    from __main__ import socketio
except:
    from app import socketio

    
logger = make_logger(__name__)


# TODO: !!!! Add auth method for sockets !!!!
@socketio.on("SEND_MESSAGE", namespace="/message")
def new_message(data):
    logger.info(f'SEND_MESSAGE Recieved {data}')
    thread_id = data['thread']
    sender_id = data['sender']
    content = data['content']
    try:
        message_dict = create_message_dict(content,sender_id,thread_id)
        create_message(message_dict)
    except KeyError as e:
        logger.error(e)
        return jsonify(error='Malformed request'), 400
    
    logger.info(f"{message_dict}")
    emit('NEW_MESSAGE',message_dict)


@socketio.on("TEST",namespace='/message')
def test_messaging2():
    logger.debug(f'/message socket test triggered {request.sid}')
    emit('test', {'data':'data'})

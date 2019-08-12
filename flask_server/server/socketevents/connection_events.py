import json
import logging


from flask import session, request, Blueprint
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect, send
from redis.exceptions import DataError


from server.auth import require_auth
from server.db.user_actions import query_user_by_id
from server.db.models import Thread
from server.redis_cache.user_cache import (
    set_user_online,
    set_user_offline,
    user_from_sid,
    get_user_by_id,
)
from server.redis_cache.message_cache import get_message_by_id
from server.logging import make_logger, log_socket

try:
    from __main__ import socketio
except:
    from app import socketio

logger = make_logger("ConnectionEvents")


@socketio.on("LOGIN_IDENTIFICATION")
def user_login(user_id):

    logged_user = query_user_by_id(user_id)
    if not logged_user:
        set_user_online(logged_user, request.sid)
        user_dict = {
            "user_id": logged_user.id,
            "username": logged_user.username,
            "online": True,
        }
        emit("USER_JOINED", user_dict, broadcast=True)
        logger.info(f"User {logged_user.id} logged on")

    else:
        logger.warning(f"User {user_id} not in database connected to socket")
        disconnect()


# TODO: add persistance of messages
@socketio.on("disconnect")
def handle_disconect():
    logger.info(f"User with SID {request.sid} has disconnected. Cleaning up.")
    try:
        user_id = set_user_offline(request.sid)
        emit("USER_LEFT", user_id, broadcast=True)
    except DataError as e:
        logger.error(e)


# ? Maybe use user_login as a callback?
@socketio.on("connect")
def handle_connect():
    # socketio.emit("CONNECTED")
    logger.info(f"URL:{request.url}")
    logger.debug("Event: connect")
    
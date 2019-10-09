import json
import logging


from flask import session, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect, send
from redis.exceptions import DataError


from server.auth import require_auth
from server.db.user_actions import query_user_by_id
from server.db.models import Thread
from server.redis_cache.user_cache import (
    # set_user_online,
    # set_user_offline,
    # user_from_sid,
    # get_user_by_id,
    # set_user_sid,
    UserEntry,
)
from server.redis_cache.message_cache import (
    # get_message_by_id,
    # create_message_dict,
    # create_message,
    # check_if_thread_exists,
    # create_thread,
    # get_next_message_id,
    # check_if_user_in_thread,
    ThreadEntry,
    MessageEntry,
)
from server.logging import make_logger
from server.utils.data_generators import FlexDict

# In a try catch block to avoid exception thrown
# during alembic migration
try:
    from __main__ import socketio
except:
    from app import socketio


logger = make_logger(__name__)


#! TODO: Connect to all currently open threads
#! TODO: CURRENTLY UNTESTABLE! Don't know how this is triggered on client
@socketio.on("connect", namespace="/message")
def message_connect():
    logger.info("Connected to /message")
    logger.info(f"User with SID({request.sid}) connected to /message namespace ")
    # emit('REQUEST_USER_IDENTIFICATION', {'DATA':'DATA'}, room=request.sid)


# Event sent by user to match the user_id to sid. This is needed because I
# don't know how to pass a payload to the connect method.
@socketio.on("SEND_IDENTIFICATION", namespace="/message")
def user_identification_sent(data):
    logger.info(f'User identification sent by {data["user"]}')
    user = UserEntry.from_user_id(data["user"]["id"])
    user.sid = request.sid
    user._set_user_online()
    # set_user_online(FlexDict(data["user"]), user_sid=request.sid)


# These handlers join the client to the thread-room
# TODO: Figure out which one of these identical functions to delete
@socketio.on("JOIN_THREAD_REQUEST", namespace="/message")
def join_thread_request(data):
    logger.info("JOIN_THREAD_REQUEST")
    logger.info(f"Client requested thread {data}")
    thread = ThreadEntry.from_id(data["thread"])
    sender = UserEntry.from_user_id(data["sender"])

    if thread.check_if_user_in_thread(sender):
        logger.info(f"Adding {sender} to thread {thread}")
        join_room(thread.thread_name)
        emit("THREAD_JOINED", {"thread": thread.to_dict()})
    else:
        emit(
            "THREAD_JOIN_FAILED",
            {"thread": data["thread"], "error": "USER NOT IN THREAD"},
        )


@socketio.on("CLIENT_THREAD_REQUEST", namespace="/message")
def client_thread_request(data):
    logger.info("CLIENT_THREAD_REQUEST")
    logger.info(f"Client requested thread {data}")
    logger.info(data["thread"])
    thread = ThreadEntry.from_id(data["thread"])
    user = UserEntry.from_sid(request.sid)

    if thread.is_user_in_thread(user):
        join_room(thread.room_name)
        emit("THREAD_JOINED", {"thread": thread.thread_id})
    else:
        emit(
            "THREAD_JOIN_FAILED",
            {"thread": thread.thread_id, "error": "USER NOT IN THREAD"},
        )


# Creates a message in a thread
# TODO: !!!! Add auth method for sockets !!!!
@socketio.on("SEND_MESSAGE", namespace="/message")
def new_message(data):
    logger.info(f"SEND_MESSAGE Recieved {data}")
    thread = ThreadEntry.from_id(data["thread"])
    sender = UserEntry.from_user_id(data["sender"])
    content = data["content"]
    try:
        message = MessageEntry(MessageEntry.next_id(incr=True), thread, sender, content)
        message.commit()
        emit("NEW_MESSAGE", message.to_dict(), room=thread.room_name)
    except KeyError as e:
        logger.error(e)
        return jsonify(error="Malformed request"), 400


@socketio.on("TEST", namespace="/message")
def test_messaging2():
    logger.debug(f"/message socket test triggered {request.sid}")
    emit("test", {"data": "data"})


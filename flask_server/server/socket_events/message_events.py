import json
import logging
import traceback

from flask import session, request, jsonify
from flask_socketio import (
    SocketIO,
    emit,
    join_room,
    leave_room,
    disconnect,
    send,
    Namespace,
    rooms,
)
from redis.exceptions import DataError


from server.auth import require_auth
from server.db.user_actions import query_user_by_id
from server.db.models import Thread
from server.redis_cache.user_cache import UserEntry
from server.redis_cache.message_cache import ThreadEntry, MessageEntry
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
        # join_room(thread.thread_name, namespace="/message")
        logger.debug("CALLING JOIN ROOM (JOIN_THREAD_REQUEST)")

        join_room(thread.thread_name)

        logger.debug(f"Rooms: {rooms()}")

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
        logger.debug("CALLING JOIN ROOM (CLIENT THREAD REQUEST)")
        join_room(thread.room_name)
        logger.debug(f"Rooms: {rooms()}")
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
    try:
        content = data["content"]
    except KeyError:
        logger.error("No content found in message")
        logger.debug(f"Contents of payload: {data}")
        content = ""
    try:

        logger.info(f"Creating MessageEntry with id: {MessageEntry.next_id()}")
        message = MessageEntry(
            MessageEntry.next_id(incr=True), thread.thread_id, sender.user_id, content
        )
        logger.info("Made MessageEntry object. Commiting...")
        message.commit()
        logger.info(f"Emitting NEW_MESSAGE id: {message.message_id}")

        emit(
            "NEW_MESSAGE",
            message.to_dict(),
            room=thread.room_name,
            namespace="/message",
        )
    except KeyError as e:
        logger.error(e)
        return jsonify(error="Malformed request"), 400


@socketio.on("REQUEST_NEW_THREAD", namespace="/message")
def new_thread(data):
    logger.info(f"REQUEST_NEW_THREAD recieved with payload {data}")

    try:
        full_members_list = [data["sender"], *data["users"]]
        existing = ThreadEntry.check_if_thread_exists(full_members_list)
        logger.debug("After geting fullmembers list")
        # TODO Return something more useful
        if existing:
            logger.info("Thread Exists")
            return existing.to_dict()
        logger.info("Creating Thread")
        thread = ThreadEntry(ThreadEntry.next_id(incr=True), users=full_members_list)
        thread.commit()

        for user in thread.users:
            logger.debug(f"User: {user}")
            logger.info(f"Getting user: {user.user_id} sid: {user.sid}")

            if user.sid != UserEntry.NO_SID:
                logger.info(f"User {user.user_id} online. Sending thread request")
                logger.info(f"User {user.user_id} has sid: {user.sid}")
                socketio.emit("SERVER_THREAD_REQUEST", thread.to_dict(), room=user.sid)
                logger.debug("CALLING JOIN ROOM")
                join_room(thread.room_name, sid=user.sid, namespace="/message")
            else:
                logger.info(f"User {user.user_id} not online")
        logger.debug(f"Rooms: {rooms()}")
        emit(
            "NEW_THREAD_CREATED",
            {"content": data["content"], **thread.to_dict()},
            room=thread.room_name,
            namesapce="/message",
        )
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.error(f"ERROR: {e}")
        socketio.emit("SERVER ERROR", {"msg": "Could not create new thread"})


@socketio.on("TEST", namespace="/message")
def test_messaging2():
    logger.debug(f"/message socket test triggered {request.sid}")
    emit("test", {"data": "data"}, room="thread-0")

    logger.debug(f"/message socket test triggered {request.sid}")

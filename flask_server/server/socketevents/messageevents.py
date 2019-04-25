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
    user_from_cache,
)
from server.redis_cache.thread_cache import check_for_thread, new_thread, get_thread_id
from server.redis_cache.message_cache import message_by_id
from server.serverlogging import make_logger

from __main__ import socketio

logger = make_logger(__name__)


def message_recieved_callback():
    pass


@socketio.on("REPORT_MESSAGE_READ", namespace="/message")
def notify_read(message_id):
    try:
        recipient_id = user_from_sid(request.sid)
        sender_id = message_by_id(message_id)["sender_id"]
        sender_sid = user_from_cache(sender_id)
        emit(
            "MESSAGE_READ",
            {"recipientId": recipient_id, "messageId": message_id},
            room=sender_sid,
        )
    except KeyError:
        logger.exception(f"Cache request for message {message_id} unsuccessful")


@socketio.on("REQUEST_NEW_THREAD")
def new_thread_request(thread):
    thread_id = check_for_thread(thread.thread_hash)
    if thread_id:
        # TODO: decide how to deal with existing threads
        pass
    else:
        thread_id = get_thread_id(thread.hash)
        thread_model = Thread(
            id=thread_id, members=thread.members, thread_hash=thread.thread_hash
        )


# TODO: !!!! Add auth method for sockets !!!!
@socketio.on("SEND_MESSAGE", namespace="/message")
def process_message(message):
    logging.info("process message")


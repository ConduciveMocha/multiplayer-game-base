import json
import base64
import time
from flask import Blueprint, request, make_response, jsonify
from flask_socketio import join_room

# from server.db import db_session
# from server.auth import make_thread_id, members_from_thread_id, require_auth
from server.db.models import User, Thread
from server.logging import make_logger
from server.redis_cache.message_cache import ThreadEntry, MessageEntry
from server.redis_cache.user_cache import UserEntry

logger = make_logger(__name__)
try:
    from __main__ import socketio
except:
    from app import socketio

    logger.error("Failed to import socketio from __main__")

message_bp = Blueprint("message", __name__, url_prefix="/message")


@message_bp.route("/test", methods=["GET", "POST"])
def message_test():
    logger.info("Test Successful")


@message_bp.route("/requestnewthread", methods=["POST"])
def request_new_thread():
    logger.info("/message/requestnewthread accessed")
    try:
        payload = request.get_json()
        logger.info(f"Payload: {payload}")
        full_members_list = [payload["sender"], *payload["users"]]
        existing = ThreadEntry.check_if_thread_exists(full_members_list)
        logger.debug("After geting fullmembers listr")
        # TODO Return something more useful
        if existing:
            logger.info("Thread Exists")
            return existing.to_dict()
        logger.info("Creating Thread")
        thread = ThreadEntry(ThreadEntry.next_id(incr=True), full_members_list)
        thread.commit()

        for user in thread.members:
            logger.debug(f"User: {user}")
            logger.info(f"Getting user: {user.user_id}")

            logger.debug(f'user sid type : {type(user["sid"])}')
            if user.sid != UserEntry.NO_SID:
                logger.info(f"User {user.user_id} online. Sending thread request")
                logger.info(f"User {user.user_id} has sid: {user.sid}")
                socketio.emit("SERVER_THREAD_REQUEST", thread.to_dict(), room=user.sid)
                join_room(room=thread.room_name, sid=user.sid)
            else:
                logger.info(f"User {user.user_id} not online")
        return jsonify(thread.to_dict()), 200
    except Exception as e:

        logger.error(f"ERROR: {e}")
        return jsonify({"error": "ERROR!"}), 503

import json
import base64
import time
from flask import Blueprint, request, make_response, jsonify
from flask_socketio import SocketIO, emit, send, Namespace

# from server.db import db_session
# from server.auth import make_thread_id, members_from_thread_id, require_auth
from server.db.models import User, Thread
from server.logging import make_logger
from server.redis_cache.message_cache import create_thread_dict, create_thread

logger = make_logger(__name__)


message_bp = Blueprint("message", __name__, url_prefix="/message")


@message_bp.route("/test", methods=["GET", "POST"])
def message_test():
    logger.info("Test Successful")


@message_bp.route("/requestnewthread", methods=["POST"])
def request_new_thread():
    logger.info("/message/requestnewthread accessed")
    try:
        payload = request.get_json()
        logger.info(f"Success: {request.get_json()}")
        thread_dict, existing = create_thread_dict(
            payload["content"], payload["sender"], payload["users"], payload["name"]
        )
        if not existing:
            new_thread_id = create_thread(thread_dict)

        return jsonify(thread_dict), 200
    except Exception as e:

        logger.error(f"ERROR: {e}")
        return jsonify({"error": "ERROR!"}), 503

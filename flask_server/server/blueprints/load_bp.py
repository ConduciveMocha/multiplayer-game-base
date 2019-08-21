import json
from flask import Blueprint, request, make_response, jsonify


from server.logging import make_logger
from server.redis_cache.user_cache import get_user_threads, get_online_users
from server.redis_cache.message_cache import get_thread_messages,get_thread_by_id


logger = make_logger(__name__)

load_bp = Blueprint("load", __name__, url_prefix="/load")


@load_bp.route("/threads", methods=["GET", "POST"])
def load_threads():
    logger.info("Loading Thread")
    try:
        payload = request.get_json()
        logger.info(f'Payload sent: {payload}')
        user_id = payload["user"]

        thread_list = get_user_threads(user_id)
        logger.info(f"Thread List: {thread_list}")

        return_payload = {"threads": {th_id: get_thread_by_id(th_id) for th_id in thread_list}}
        logger.info(f"Returning: {return_payload}")
        return jsonify(return_payload)
    except Exception as e:
        logger.error(f"ERROR: {e}")
        return jsonify(error="Could not load threads")


@load_bp.route("/thread-messages", methods=["GET", "POST"])
def load_thread_messages():
    logger.info("Loading messages")
    try:
        payload = request.get_json()
        
        logger.info(f'Payload sent: {payload}')
        thread_id = payload["thread"]
        return_payload = {
            "messages": get_thread_messages(thread_id)
        }
        logger.info(f"Returning: {return_payload}")
        return jsonify(return_payload)
    except Exception as e:
        logger.error(f"ERROR: {e}")
        return jsonify(error="Error loading thread messages")


@load_bp.route("/user-list", methods=["GET", "POST"])
def load_user_list():
    logger.info("Loading user list")
    try:
        return_payload = {"friends": {}, "online": get_online_users()}
        logger.info(f"Returning: {return_payload}")
        return jsonify(return_payload)

    except Exception as e:
        logger.error(f"ERROR: {e}")
        return jsonify(error="Error loading users")


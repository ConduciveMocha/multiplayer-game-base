import json
import traceback


from flask import Blueprint, request, make_response, jsonify


from server.logging import make_logger
from server.redis_cache.user_cache import UserEntry
from server.redis_cache.message_cache import ThreadEntry, MessageEntry


logger = make_logger(__name__)

load_bp = Blueprint("load", __name__, url_prefix="/load")


@load_bp.route("/threads", methods=["GET", "POST"])
def load_threads():
    logger.info("Loading Thread")
    try:
        payload = request.get_json()
        logger.info(f"Payload sent: {payload}")
        user = UserEntry.from_user_id(payload["user"])
        logger.debug("Loaded user")
        # thread_list = get_user_threads(user.user_id)
        thread_list = user.threads
        logger.info("Hey Nate!")
        logger.info(f"Thread List: {thread_list}")
        logger.debug(f"{[thread.__dict__ for thread in thread_list]}")
        return_payload = {
            "threads": {thread.thread_id: thread.to_dict() for thread in thread_list}
        }
        logger.info(f"Returning: {return_payload}")
        return jsonify(return_payload)
    except Exception as e:
        logger.error(f"ERROR: ({type(e)}) {e}")
        traceback.print_tb(e)
        return jsonify(error="Could not load threads")


@load_bp.route("/thread-messages", methods=["GET", "POST"])
def load_thread_messages():
    logger.info("Loading messages")
    try:
        payload = request.get_json()

        logger.info(f"Payload sent: {payload}")
        thread_id = payload["thread"]
        thread = ThreadEntry(thread_id)
        return_payload = {
            "messages": {
                message.message_id: message.to_dict() for message in thread.messages
            }
        }
        logger.info(f"Returning: {return_payload}")
        return jsonify(return_payload)
    except Exception as e:
        logger.error(f"ERROR: {e}")
        traceback.print_tb(e.__traceback__)

        return jsonify(error="Error loading thread messages")


@load_bp.route("/user-list", methods=["GET", "POST"])
def load_user_list():
    logger.info("Loading user list")
    try:
        # logger.info(f"Return value of get_online_users: {UserEntry.get_online_users()}")
        return_payload = {"friends": {}, "online": UserEntry.get_online_users()}
        # logger.info(f"Returning: {return_payload}")
        return jsonify(return_payload)

    except Exception as e:
        logger.error(f"ERROR: {e}")
        traceback.print_tb(e.__traceback__)

        return jsonify(error="Error loading users")


@load_bp.route("game-objects", methods=["GET", "POST"])
def load_game_objects():
    logger.info("Loading game objects")
    try:
        payload = request.get_json()
        env_id = payload["env"]
    except AttributeError:
        return jsonify(error="Malformed request: `env` was not specified")
    try:
        return get_environment_objects(env_id)
    except Exception as e:
        logger.error("Error thrown getting environment id")
        traceback.print_tb(e.__traceback__)

        return jsonify(error="Error retrieving game objects")


import json
import base64
import time
from flask import Blueprint, request, make_response, jsonify
from flask_socketio import SocketIO, emit, send, Namespace

# from server.db import db_session
# from server.auth import make_thread_id, members_from_thread_id, require_auth
from server.db.models import User, Thread
from server.logging import make_logger

logger = make_logger(__name__)



message_bp = Blueprint('message', __name__, url_prefix='/message')


@message_bp.route('/test', methods=['GET','POST'])
def message_test():
    logger.info('Test Successful')


def match_users_to_threads(user_list,thread_list):
    for thread in thread_list:
        if all(user in thread.users for user in user_list) \
        and len(user_list) == len(thread.users):
            return thread        
    return None

@message_bp.route('/requestnewthread', methods=['POST'])
def request_new_thread():
    logger.info('/message/requestnewthread accessed')
    try:
        logger.info(f"Success: {request.get_json()}")
        return jsonify({'test':'test'}),200
    except Exception as e:

        logger.error(f'ERROR: {e}')
        return jsonify({'error':'ERROR!'}), 503

import json
import logging
import traceback

from flask import session, request, jsonify
from flask_socketio import SocketIO, emit, send


from server.logging import make_logger
from server.db.game_actions import remove_from_user_inventory, get_user_inventory

try:
    from __main__ import socketio
except:
    from app import socketio

logger = make_logger(__name__)


@socketio.on("connect", namespace="/inventory")
def inventory_connect():
    logger.info("Connected to /inventory")
    emit("Test", {"test": "test"})


@socketio.on("LOAD_USER_OBJECTS", namespace="/inventory")
def load_user_objects(data):
    try:
        user_inventory = get_user_inventory(data["userId"])
        emit("LOAD_USER_INVENTORY_CONFIRMED", user_inventory)
    except Exception as e:
        emit("LOAD_USER_INVENTORY_ERROR", {"errorMessage": str(e)})


@socketio.on("ACQUIRE_ITEM", namespace="/inventory")
def acquire_item(data):
    emit("Test", {"test": "test"})


@socketio.on("DROP_ITEM", namespace="/inventory")
def drop_item(data):
    logger.info(f"Recieved DROP_ITEM: {data}")
    item_id, user_id = data["itemId"], data["userId"]
    return_value = remove_from_user_inventory(
        item_id, user_id, raise_underflow_error=True
    )
    emit("DROP_ITEM_CONFIRMED", return_value)


@socketio.on("DELETE_ITEM", namespace="inventory")
def delete_item(data):
    emit("Test", {"test": "test"})

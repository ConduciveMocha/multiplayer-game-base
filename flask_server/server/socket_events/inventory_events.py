import json
import logging
import traceback

from flask import request, jsonify
from flask_socketio import SocketIO, emit, send

from server.logging import make_logger


try:
    from __main__ import socketio
except:
    from app import socketio

logger = make_logger(__name__)


@socketio.on("connect", namespace="/inventory")
def inventory_connect():
    logger.info("Connected to /inventory")


@socketio.on("ACQUIRE_ITEM", namespace="/inventory")
def acquire_item(data):
    pass


@socketio.on("DROP_ITEM", namespace="/inventory")
def drop_item(data):
    pass


@socketio.on("DELETE_ITEM", namespace="inventory")
def delete_item(data):
    pass

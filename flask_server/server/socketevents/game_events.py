import json

from flask import session, jsonify
from flask_socketio import SocketIO, emit, join_room,leave_room,disconnect,send

from server.logging import make_logger

logger = make_logger(__name__)


try:
    from __main__ import socketio
except:
    logger.critical('Could not import socketio from __main__ (in game_events.py). Server will crash.')

@socketio.on("PLAYER_KEYED", namespace='/game')
def player_keyed(data):
    logger.info(f'Player Key Sent: {data}')
    emit("TEST",{"data":"data"})
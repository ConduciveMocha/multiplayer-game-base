import json

from flask import session, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect, send

from server.logging import make_logger

logger = make_logger(__name__)


try:
    from __main__ import socketio
except:
    logger.critical(
        "Could not import socketio from __main__ (in game_events.py). Server will crash."
    )

test_movement_dict = {
    "ArrowUp": [0, -1],
    "ArrowLeft": [-1, 0],
    "ArrowRight": [1, 0],
    "ArrowDown": [0, 1],
}




def update_pos(data):
    delta = test_movement_dict[data["key"]]
    data["playerObject"]["x"] += delta[0]
    data["playerObject"]["y"] += delta[1]
    return data["playerObject"]


@socketio.on("PLAYER_KEYED", namespace="/game")
def player_keyed(data):

    logger.info(f"Player Key Sent: {data}")
    emit("UPDATE_GAMESTATE", {"updatedObjects": [update_pos(data)]})


import json

from flask import session, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect, send
from server.db.game_actions import move_game_object
from server.logging import make_logger
from server.game.geometric_types.vector import Vector
logger = make_logger(__name__)


try:
    from __main__ import socketio
except:
    #! THIS IS USED TO PREVENT DB MIGRATION TO GO THROUGH!!!!!
    from app import socketio

test_movement_dict = {
    "ArrowUp": Vector(0, -1),
    "ArrowLeft": Vector(-1, 0),
    "ArrowRight": Vector(1, 0),
    "ArrowDown": Vector(0, 1),
}



def update_pos(data):
    delta = test_movement_dict[data["key"]]
    
    return move_game_object(0, delta)


@socketio.on("PLAYER_KEYED", namespace="/game")
def player_keyed(data):

    logger.info(f"Player Key Sent: {data}")
    emit("UPDATE_GAMESTATE", {"updatedObjects": [update_pos(data)]})


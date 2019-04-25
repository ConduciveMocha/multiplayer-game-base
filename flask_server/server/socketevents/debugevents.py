import logging

from flask import request
from flask_socketio import emit
from server.serverlogging import make_logger
from __main__ import socketio

logger = make_logger(__name__)


@socketio.on("SOCKET_TEST")
def test_connection():
    logging.debug("Connection good")
    emit("MESSAGE SENT", {"test": "test"})
    emit("MESSAGE SENT", {"test2": "test2"}, room=request.sid)


@socketio.on("NAMESPACE_TEST", namespace="/message")
def test_message():
    logging.debug("Namespace connection good")
    emit("MESSAGE SENT", {"message test": True})
    emit("MESSAGE SENT", {"TEST": "TEST"}, room=request.sid)

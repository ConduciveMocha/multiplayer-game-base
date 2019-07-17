import logging
from flask import request
from flask_socketio import emit, send
from server.logging import make_logger, log_socket

logger = make_logger(__name__)

try:
    from __main__ import socketio
except:
    from app import socketio
    logger.error("Failed to import socketio from __main__")


@socketio.on("SOCKET_TEST", namespace="/")
def test_connection():
    socketio.emit("TEST_SUCCESSFUL", "test_connection", namespace="/", broadcast=True)


@socketio.on("NAMESPACE_TEST", namespace="/message")
@log_socket
def test_namespace(data):
    logger.debug(f"Namespace connection good")


    socketio.emit(
        "TEST_SUCCESSFUL", "test_namespace", namespace="/message", broadcast=True
    )

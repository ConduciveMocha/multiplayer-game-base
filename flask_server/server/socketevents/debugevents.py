import logging
from flask import request
from flask_socketio import emit, send
from server.logging import make_logger, log_socket

logger = make_logger(__name__)

try:
    # For the love of everything that is holy, do not touch 
    # this line of code. You will fuck away another entire
    # night trying to figure out what the fuck is wrong
    from __main__ import socketio
except:
    from app import socketio
    logger.error("Failed to import socketio from __main__")

print('here')
@socketio.on("SOCKET_TEST",namespace="/")
def test_connection(data):
    logger.debug('SOCKET_TEST Recieved')
    socketio.emit("test", {'test':'test_successful'},  broadcast=False)
    
@socketio.on("NAMESPACE_TEST", namespace="/message")
def test_namespace(data):

    logger.debug(f"Namespace connection good {data}")


    socketio.emit(
        "TEST_SUCCESSFUL", "test_namespace", namespace="/message", broadcast=True
    )

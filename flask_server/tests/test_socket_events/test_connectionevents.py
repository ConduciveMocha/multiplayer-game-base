import pytest
import logging
from server.logging import make_test_logger, log_test

logger = make_test_logger(__name__)


@log_test(logger)
def test_connect(socketio_client):
    app, client = socketio_client()
    with app.test_request_context("/"):
        client.emit("connect")
        resp = client.get_received()[0]
        assert resp["name"] == "CONNECTED"
        assert len(resp["args"]) == 1
        assert resp["args"][0] is None
        assert resp["namespace"] == "/"


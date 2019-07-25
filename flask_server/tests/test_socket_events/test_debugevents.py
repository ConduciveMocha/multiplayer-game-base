import pytest
import logging

from server.logging import log_test, make_test_logger

logger = make_test_logger(__name__)


@log_test(logger)
def test_connection_event(socketio_client):
    app, client = socketio_client()

    with app.test_request_context("/"):
        client.emit("SOCKET_TEST")

        resp = client.get_received()
        connect_resp, result_resp = resp

        # Check that connection handler ran
        assert connect_resp["name"] == "CONNECTED"
        # Check that there are no extra return values
        assert len(connect_resp["args"]) == 1
        # Check that connection handler had no return
        assert connect_resp["args"][0] is None
        # Check namespace of connection handler
        assert connect_resp["namespace"] == "/"

        # Check server returned success message
        assert result_resp["name"] == "TEST_SUCCESSFUL"
        # Check that there are no extra return values
        assert len(result_resp["args"]) == 1
        # Check function name of event handler
        assert result_resp["args"][0] == "test_connection"
        # Check namespace
        assert result_resp["namespace"] == "/"


@log_test(logger)
def test_namespace_event(socketio_client):

    app, client = socketio_client("/test")

    with app.test_request_context("/"):
        client.emit("NAMESPACE_TEST", namespace="/test")
        resp = client.get_received(namespace="/test")[0]

        # Check server returned success message
        assert resp["name"] == "TEST_SUCCESSFUL"
        # Check that there are no extra return values
        assert len(resp["args"]) == 1
        # Check function name of event handler
        assert resp["args"][0] == "test_namespace"
        # Check namespace
        assert resp["namespace"] == "/test"

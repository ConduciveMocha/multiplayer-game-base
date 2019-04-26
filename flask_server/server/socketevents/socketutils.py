import logging
from functools import wraps

from flask import request
from flask_socketio import emit, send
from server.logging import log_socket, make_logger

try:
    from __main__ import socketio
except:
    from app import socketio
_emit = socketio.emit
_send = socketio.send
_on = socketio.on


def get_wrapped_emit():
    socket_logger = make_logger(
        "socketevent", console_format="%(levelname)s:%(name)s: %(msg)s"
    )
    line_padding = 18 * " " + "-"

    @wraps(socketio.emit)
    def wrap_emit(*args, **kwargs):
        try:
            print_namespace = str(kwargs["namespace"]) if kwargs["namespace"] else "/"
        except KeyError:
            print_namespace = "/"
        try:
            print_data = f"\n{line_padding}Payload: {args[1]}" if args[1] else ""
        except IndexError:
            print_data = ""

        socket_logger.debug(
            f"EMIT:{args[0]}: Sending to {request.sid} on namespace {print_namespace}){print_data}"
        )
        _emit(*args, **kwargs)

    return wrap_emit


def get_wrapped_send():
    socket_logger = make_logger(
        "socketevent", console_format="%(levelname)s:%(name)s: %(msg)s"
    )
    line_padding = 18 * " " + "-"

    @wraps(socketio.send)
    def wrap_send(*args, **kwargs):
        try:
            print_namespace = str(kwargs["namespace"]) if kwargs["namespace"] else "/"
        except KeyError:
            print_namespace = "/"
        try:
            print_data = f"\n{line_padding}Payload: {args[0]}" if args[0] else ""
        except IndexError:
            print_data = ""

        socket_logger.debug(
            f"SEND: Sending to {request.sid} on namespace {print_namespace}){print_data}"
        )
        _send(*args, **kwargs)

    return wrap_send


def get_wrapped_on():
    def wrap_on(*args, **kwargs):
        @wraps(socketio.on)
        def wrapper(func):
            return _on(*args, **kwargs)(log_socket(func))

        return wrapper

    return wrap_on


def configure_socket_functions(config, logger=None):
    if logger is True:
        logger = make_logger("APPFACTORY")
    elif logger is None:
        logger = make_logger("CONF:SOCKETFUNCTIONS")
        logger.setLevel(logging.ERROR)

    try:
        if config.LOG_SOCKETS_INCOMING:
            socketio.on = get_wrapped_on()
            logger.debug("Logging added to all incoming socket event")
        else:
            logger.debug(
                "Logging will not be added to incoming socket events by default. Use `log_socket` from server.logging to log incoming events."
            )
    except AttributeError:
        logger.debug(
            "Logging will not be added to incoming socket events by default. Use `log_socket` from server.logging to log incoming events."
        )

    try:
        if config.LOG_SOCKETS_OUTGOING:
            socketio.emit = get_wrapped_emit()
            socketio.send = get_wrapped_send()
            logger.debug("Logging added to all outgoing socket events")
        else:
            log_outgoing = False
            logger.debug(
                "Logging will not be added to outgoing socket events by default. Call `get_wrapped_emit()` and `get_wrapped_send()` from server.socketevents.socketutils to get a functions that log outgoing events."
            )
    except AttributeError:
        try:

            if config.WRAP_SOCKETS_EMIT:
                socketio.emit = get_wrapped_emit()
                logger.debug("Logging added to socketio.emit")
            else:
                logger.debug(
                    "Logging will not be added to socketio.emit by default. Call `get_wrapped_emit()` from server.socketevents.socketutils to get an emit function that logs outgoing events."
                )
        except AttributeError:
            logger.debug(
                "Logging will not be added to socketio.emit by default. Call `get_wrapped_emit()` from server.socketevents.socketutils to get an emit function that logs outgoing events."
            )

        try:
            if config.WRAP_SOCKETS_SEND:
                socketio.send = get_wrapped_send()
                logger.debug("Logging added to socketio.send")
            else:
                logger.debug(
                    "Logging will not be added to socketio.send by default. Call `get_wrapped_send()` from server.socketevents.socketutils to get a send function that logs outgoing events."
                )
        except AttributeError:
            logger.debug(
                "Logging will not be added to socketio.send by default. Call `get_wrapped_send()` from server.socketevents.socketutils to get a send function that logs outgoing events."
            )


# socketio.on(*args,**kwargs)
#       ---> log_socket(func)
#               --->func(*args,**kwargs)

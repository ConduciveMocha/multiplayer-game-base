import logging
import json
from sys import stdout
from functools import wraps

logging.basicConfig(
    filename="logs/serverlog.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s:%(name)s:  %(message)s",
)

default_console_fmt = logging.Formatter("%(levelname)s:%(filename)s:  %(msg)s")
default_file_fmt = logging.Formatter(
    "%(asctime)s - %(levelname)s:%(name)s:  %(message)s"
)


def make_socket_loggers(
    socketio_console_level=logging.WARN,
    socketio_file_level=logging.DEBUG,
    socketio_format=default_file_fmt,
    engineio_console_level=logging.WARN,
    engineio_file_level=logging.DEBUG,
    engineio_format=default_file_fmt,
):
    """
    Makes the socketio and engineio loggers

    Defaults to overwriting log files. Change this for production
    
    """

    # Socketio logger config
    socketio_logger = logging.getLogger("socketlog")
    if not socketio_logger.handlers:
        socketio_con_h = logging.StreamHandler()
        socketio_con_h.setLevel(socketio_console_level)
        socketio_logger.addHandler(socketio_con_h)

        socketio_file_h = logging.FileHandler("logs/socketio.log")
        socketio_formatter = socketio_format
        socketio_file_h.setFormatter(socketio_formatter)
        socketio_file_h.setLevel(logging.INFO)
        socketio_logger.addHandler(socketio_file_h)

    # Engineio logger config
    engineio_logger = logging.getLogger("engineiolog")

    if not engineio_logger.handlers:
        engineio_con_h = logging.StreamHandler(stdout)
        engineio_con_h.setLevel(engineio_console_level)
        engineio_logger.addHandler(engineio_con_h)

        engineio_file_h = logging.FileHandler("logs/engineio.log")

        engineio_file_h.setFormatter(engineio_format)
        engineio_file_h.setLevel(logging.INFO)
        engineio_logger.addHandler(engineio_file_h)

    return socketio_logger, engineio_logger


def make_logger(
    name,
    console_level=logging.DEBUG,
    file_level=logging.DEBUG,
    console_format=default_console_fmt,
    file_format=default_file_fmt,
):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        console_handler.setFormatter(console_format)
        # file_handler = logging.FileHandler("logs/serverlog.log")
        # file_handler.setLevel(console_level)
        # file_handler.setFormatter(file_format)
        logger.addHandler(console_handler)
        # logger.addHandler(file_handler)
    return logger


serverlogger = make_logger("server")


def log_funcname(logger):
    def decorator(func):
        def wrapped(*args, **kwargs):
            logger.debug("%(asctime)s - Calling %(funcName)s")
            return func(*args, **kwargs)

        wrapped.__name__ = func.__name__
        return wrapped

    return decorator


def try_call(func, *args, debug_logger=None, **kwargs):
    if not debug_logger:
        debug_logger = logging.getLogger(func.__name__)
    try:
        ret = func(*args, **kwargs)
        debug_logger.info(
            f'{func.__name__} executed properly.\nargs:{args}\nkwargs:{kwargs}{"ret:" + str(ret) if ret else ""}'
        )
        return ret, True

    except Exception as e:
        debug_logger.error(
            f"{func.__name__} failed with {type(e)}\nargs:{args}\nkwargs:{kwargs}\nexception:\n{e}"
        )
        return None, False


def request_log(request):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            serverlogger.info(
                f"SERVER: {request.method.upper()} REQUEST: {request.base_url} "
            )
            if len(request.args) is not 0:
                serverlogger.debug(f"SERVER: PAYLOAD: {request.args}")
            try:
                resp = func(*args, **kwargs)
                serverlogger.info(
                    f"SERVER: {request.method.upper()} RESPONSE: {request.base_url} CODE: {resp[1]}"
                )
                serverlogger.debug(
                    f'SERVER: {request.method.upper()} PAYLOAD: {str(resp[0])[:50]}{ "... "+resp[0][-1] if len(resp[0]) > 75 else ""} '
                )
                return resp
            except Exception as e:
                serverlogger.error(f"SERVER: Exception: {e}")
                return json.dumps({"error": "Invalid Request"}), 400

        wrapped.__name__ = func.__name__
        return wrapped

    return decorator


def db_log(db_method, db_types, inspect_args=False):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            serverlogger.info(
                f'MYSQL: RUNNING {db_method.upper} WITH TYPES {", ".join(db_types).upper()}'
            )
            if inspect_args:
                logging.debug(f"MYSQL:ARGS: *args: {args}")
                serverlogger.debug(f"MYSQL:KWARGS: *kwargs: {kwargs}")
            try:
                resp = func(*args, **kwargs)
                serverlogger.info(
                    f'MYSQL: FINISHED {db_method.upper()} WITH TYPES {", ".join(db_types).upper()}'
                )
                return resp
            except Exception as e:
                serverlogger.error(f"MYSQL:EXCEPTION: {e}")

        wrapped.__name__ = func.__name__
        return wrapped

    return decorator


def log_socket(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        serverlogger.debug(
            f"Recieved socked message on route {func.__name__}\nargs:{args}\nkwargs{kwargs}"
        )
        return func(*args, **kwargs)

    return wrapper


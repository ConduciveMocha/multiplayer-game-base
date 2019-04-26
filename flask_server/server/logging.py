import logging
import json
from sys import stdout
from functools import wraps

# BASIC LOGGING CONFIG:
logging.basicConfig(
    filename="logs/serverlog.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(msecs)d - %(levelname)s:%(name)s:  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# Default log formats
default_console_fmt = logging.Formatter("%(levelname)s:%(filename)s:  %(msg)s")
default_file_fmt = logging.Formatter(
    "%(asctime)s:%(msecs)d - %(levelname)s:%(name)s:  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
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

    # ? Make sure this is necessary
    # Avoids adding duplicate handlers
    if not socketio_logger.handlers:
        # Console Handler
        socketio_con_h = logging.StreamHandler()
        socketio_con_h.setLevel(socketio_console_level)
        socketio_logger.addHandler(socketio_con_h)

        # File Handler
        socketio_file_h = logging.FileHandler("logs/socketio.log")
        socketio_formatter = socketio_format
        socketio_file_h.setFormatter(socketio_formatter)
        socketio_file_h.setLevel(logging.INFO)
        socketio_logger.addHandler(socketio_file_h)

    # Engineio logger config
    engineio_logger = logging.getLogger("engineiolog")

    # Avoids adding duplicate handlers
    if not engineio_logger.handlers:
        # Console Handler
        engineio_con_h = logging.StreamHandler(stdout)
        engineio_con_h.setLevel(engineio_console_level)
        engineio_logger.addHandler(engineio_con_h)

        # File handler
        engineio_file_h = logging.FileHandler("logs/engineio.log")
        engineio_file_h.setFormatter(engineio_format)
        engineio_file_h.setLevel(logging.INFO)
        engineio_logger.addHandler(engineio_file_h)

    return socketio_logger, engineio_logger


def make_logger(name, console_level=logging.DEBUG, console_format=default_console_fmt):
    """
    Creates a logger with specified name and correct format.
    """
    # Cast to log objects
    if isinstance(console_format, str):
        console_format = logging.Formatter(console_format)

    logger = logging.getLogger(name)

    # Prevents double logging
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
    return logger


def make_test_logger(name):
    logger = logging.getLogger("TEST:" + name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        file_handler = logging.FileHandler("logs/testlog.log")
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter("%(name)s:%(funcName)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    return logger


def log_function(logger, log_all=False, log_args=False, log_return=False):
    """
    Decorator that logs the name of the wraped function
    """

    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if log_all or log_args:
                print_args = f"\n\t\t-args: {args}"
                print_kwargs = f"\n\t\t-kwargs: {kwargs}"
            else:
                print_args = ""
                print_kwargs = ""
            logger.debug(f"Calling {func.__name__}{print_args}{print_kwargs}")
            if log_all or log_return:
                ret = func(*args, **kwargs)
                logger.debug(f"Return of {func.__name__}: {ret}")
                return ret
            else:
                return func(*args, **kwargs)

        return wrapped

    return decorator


def try_call(func, *args, debug_logger=None, **kwargs):
    """
    Wraps function call in a try catch block and logs the result or exception
    """
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
    """
    Decorator that logs the server request passed into the wrapped function
    """

    def decorator(func):
        logger = make_logger("REQUESTLOG")

        @wraps(func)
        def wrapped(*args, **kwargs):
            logger.info(
                f"SERVER: {request.method.upper()} REQUEST: {request.base_url} "
            )
            if len(request.args) is not 0:
                logger.debug(f"SERVER: PAYLOAD: {request.args}")
            try:
                resp = func(*args, **kwargs)
                logger.info(
                    f"SERVER: {request.method.upper()} RESPONSE: {request.base_url} CODE: {resp[1]}"
                )
                logger.debug(
                    f'SERVER: {request.method.upper()} PAYLOAD: {str(resp[0])[:50]}{ "... "+resp[0][-1] if len(resp[0]) > 75 else ""} '
                )
                return resp
            except Exception as e:
                logger.error(f"SERVER: Exception: {e}")
                return json.dumps({"error": "Invalid Request"}), 400

        return wrapped

    return decorator


# TODO: Refactor or remove this
def db_log(db_method, db_types, inspect_args=False):
    """
    Decorator that logs arguments and results of a db function
    """
    logger = make_logger("DBFUNCTION")

    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            logger.info(
                f'MYSQL: RUNNING {db_method.upper} WITH TYPES {", ".join(db_types).upper()}'
            )
            if inspect_args:
                logging.debug(f"MYSQL:ARGS: *args: {args}")
                logger.debug(f"MYSQL:KWARGS: *kwargs: {kwargs}")
            try:
                resp = func(*args, **kwargs)
                logger.info(
                    f'MYSQL: FINISHED {db_method.upper()} WITH TYPES {", ".join(db_types).upper()}'
                )
                return resp
            except Exception as e:
                logger.error(f"MYSQL:EXCEPTION: {e}")

        wrapped.__name__ = func.__name__
        return wrapped

    return decorator


def log_socket(func):
    """
    Decorator that wraps functions that recieve socket events
    """

    socket_logger = make_logger(
        "socketevent", console_format="%(levelname)s:%(name)s: %(msg)s"
    )
    line_padding = " " * 18 + "-"

    @wraps(func)
    def wrapper(*args, **kwargs):
        print_args = f"\n{line_padding}args:{args}" if args else ""
        print_kwargs = f"\n{line_padding}kwargs:{kwargs}" if kwargs else ""
        socket_logger.debug(
            f"Recieved socket event: `{func.__name__}`{print_args}{print_kwargs}"
        )
        func_return = func(*args, **kwargs)
        socket_logger.debug(f"Returning from event: `{func.__name__}`")

    return wrapper


def log_test(logger=None):
    if logger is None:
        logger = make_test_logger("DEFAULT")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Running Test: {func.__name__}")
            ret = func(*args, **kwargs)
            logger.info(f"Test Completed: {func.__name__}")
            return ret

        return wrapper

    return decorator


# TODO: Refactor this out of the package
serverlogger = make_logger("server")

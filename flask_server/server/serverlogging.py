import logging

import json


logging.basicConfig(level=logging.DEBUG)
serverlogger = logging.getLogger(name="ServerLog")


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

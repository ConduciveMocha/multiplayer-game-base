import logging

import json

def create_logger():
    

logging.basicConfig(level=logging.DEBUG)
server_logger = logging.getLogger(name='ServerLog')


def request_log(request):
    def decorator(func):
        def wrapped(*args, **kwargs):
            server_logger.info(
                f'SERVER: {request.method.upper()} REQUEST: {request.base_url} ')
            if len(request.args) is not 0:
                server_logger.debug(f'SERVER: PAYLOAD: {request.args}')
            try:
                resp = func(*args, **kwargs)
                server_logger.info(
                    f'SERVER: {request.method.upper()} RESPONSE: {request.base_url} CODE: {resp[1]}')
                server_logger.debug(
                    f'SERVER: {request.method.upper()} PAYLOAD: {str(resp[0])[:50]}{ "... "+resp[0][-1] if len(resp[0]) > 75 else ""} ')
                return resp
            except Exception as e:
                server_logger.error(f'SERVER: Exception: {e}')
                return json.dumps({'error': 'Invalid Request'}), 400
        wrapped.__name__ = func.__name__
        return wrapped
    return decorator


def db_log(db_method, db_types, inspect_args=False):
    def decorator(func):
        def wrapped(*args, **kwargs):
            server_logger.info(
                f'MYSQL: RUNNING {db_method.upper} WITH TYPES {", ".join(db_types).upper()}')
            if inspect_args:
                loggin.debug(f'MYSQL:ARGS: *args: {args}')
                server_logger.debug(f'MYSQL:KWARGS: *kwargs: {kwargs}')
            try:
                resp = func(*args, **kwargs)
                server_logger.info(
                    f'MYSQL: FINISHED {db_method.upper()} WITH TYPES {", ".join(db_types).upper()}')
                return resp
            except Exception as e:
                server_logger.error(f'MYSQL:EXCEPTION: {e}')
        wrapped.__name__ = func.__name__
        return wrapped
    return decorator

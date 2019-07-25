import json
import logging

from functools import wraps

from flask import request, jsonify, g
from werkzeug.exceptions import BadRequest

from server.logging import make_logger

INTERNAL_SERVER_ERROR = json.dumps({"error": "Internal Server Error"}), 500
# INVALID_REQUEST_ERROR = jsonify(error='Invalid Request'), 400


def make_bad_request(reason=None):
    resp_dict = {"error": "Bad Request"}
    if reason:
        resp_dict["reason"] = reason
    return json.dumps(resp_dict), 400


def required_or_400(required=[], logger=make_logger("required_or_400")):
    """Decorator that adds required parameters from the 
       request object to the global context
    """

    if isinstance(required, str):
        required = [required]
    elif not isinstance(required, list):
        raise TypeError("`required` must be a list or str")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            try:
                payload = request.get_json()

                for req_item in required:
                    if req_item in g.__dict__:
                        logger.critical(f"`g` contained `{req_item}` before definition")
                        return INTERNAL_SERVER_ERROR
                    g.__setattr__(req_item, payload[req_item])

            except BadRequest:

                if logger:
                    logger.debug(f"Throwing `BadRequest`")
                    logger.error(f"Could not parse JSON")
                return make_bad_request(f"Requires JSON Object")

            except KeyError:
                if logger:
                    logger.debug(f"Throwing `KeyError`")
                    logger.error(f"Could not acquire {req_item} from request")
                return make_bad_request(f"Missing Parameter: {req_item}")
            except Exception as e:
                if logger:
                    logger.debug(f"Throwing {type(e)}")
                    logger.error("Error parsing request")
                return make_bad_request(reason=f"Requires JSON Object")
            return func(*args, **kwargs)

        return wrapper

    return decorator

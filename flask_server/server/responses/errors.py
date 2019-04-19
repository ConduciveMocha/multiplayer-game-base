import json

INTERNAL_SERVER_ERROR = json.dumps({'error': 'Internal Server Error'}), 500
# INVALID_REQUEST_ERROR = jsonify(error='Invalid Request'), 400


def make_bad_request(reason=None):
    resp_dict = {'error': 'Bad Request'}
    if reason:
        resp_dict['reason'] = reason
    return json.dumps(resp_dict), 400

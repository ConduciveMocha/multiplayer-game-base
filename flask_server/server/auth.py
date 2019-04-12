import json
import jwt
from flask import jsonify
from datetime import datetime, timedelta

from server.loggers.serverlogger import server_logger

#TODO Replace with actual key
JWT_SECRET = 'secret' 
JWT_ALGORITHMS = ['HS256']
JWT_ISS = 'http://localhost:5000'
JWT_EXP_DELTA_SECONDS = 20

"""
    Returns a JWT for a giver user id
"""
def login_jwt(user_id,iss=JWT_ISS, iat=None, exp_delta=JWT_EXP_DELTA_SECONDS):

    payload = {
        'iss': iss,
        'user_id':user_id,
        'iat': iat if iat else datetime.utcnow(),
        'exp':datetime.utcnow() + timedelta(seconds=exp_delta)
    }
    token = jwt.encode(payload,JWT_SECRET,JWT_ALGORITHMS[0])
    return token


def verify_jwt(token,user_id=None, decoded=False):
    if not token:
        server_logger.info('JWT Error: no token')
        return False
    # Catch errors from jwt decode and KeyError
    try:
        # Decodes if necessary
        payload = token if decoded else jwt.decode(token, key=JWT_SECRET, algorithms=JWT_ALGORITHMS)
        
        # Bad Issuer
        if payload['iss'] != JWT_ISS:
            server_logger.info('JWT Error: bad issuer')
            return False
        # Bad Issue Time
        elif datetime.utcfromtimestamp(payload['iat']) > datetime.utcnow():
            server_logger.info('JWT Error: bad iat')
            return False
        # Bad User id
        elif user_id is not None and payload['user_id'] != user_id:
            server_logger.info('JWT Error: bad user_id')
            return False
    # jwt.decode failed
    except jwt.DecodeError as e:
        server_logger.info('JWT Error: decode error')
        return False
    # Signature invalid
    except jwt.ExpiredSignatureError as e:
        server_logger.info('JWT Error: expired signature')
        return False
    # Bad Payload
    except KeyError as e:
        server_logger.info('JWT Error: bad payload')
        return False
    return True
    
"""
    Decorator that wraps routes requiring an Auth Token
"""
def require_auth(request):
    def decorator(func):
        def wrapper(*args,**kwargs):
            token = request.headers.get('authorization',None)
            if not verify_jwt(token,user_id=payload['user_id']):
                return json.dumps({'error':'Token is invalid'}), 400
            else:
                return func(*args,**kwargs)
        return wrapper
    return decorator


def make_thread_id(members):
    enc = '_'.join(map(lambda x: str(x), members.sort()))
    return base64.b64encode(enc.encode('utf-8')).decode('utf-8')


def members_from_thread_id(thread_id):
    dec = base64.b64decode(thread_id).decode('utf-8')
    dec = dec.split('_')
    members = []
    for i, m in enumerate(dec):
        if i == 0:
            members.append(int(m))
        else:
            members.append(members[-1] + int(m))
    return members

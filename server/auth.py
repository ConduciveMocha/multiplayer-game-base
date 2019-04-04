import json
import jwt
from flask import jsonify
from datetime import datetime, timedelta


#TODO Replace with actual key
JWT_SECRET = 'secret' 
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 20

"""
    Returns a JWT for a giver user id
"""
def login_jwt(user_id):
    payload = {
        'iss': 'http://localhost:5000',
        'user_id':user_id,
        'iat': datetime.utcnow(),
        'exp':datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload,JWT_SECRET,JWT_ALGORITHM).decode('utf-8')
    return token


"""
    Decorator that wraps routes requiring an Auth Token
"""
def require_auth(request):
    def decorator(func):
        def wrapper(*args,**kwargs):
            
            token = request.headers.get('authorization',None)
            if not token:
                return 'auth error'
            try:
                payload = jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return json.dumps({'error':'Token is invalid'}), 400

            return func(*args,id=payload['user_id'],**kwargs)
        return wrapper
    return decorator
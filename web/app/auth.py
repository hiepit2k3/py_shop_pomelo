from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask import request
from exceptions import InvalidCredentialsException,ForbiddenException

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            raise InvalidCredentialsException("Token is invalid")
        return f(*args, **kwargs)
    return decorated

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['role'] != role:
                raise ForbiddenException("403 Forbidden")
            return fn(*args, **kwargs)
        return wrapper
    return decorator
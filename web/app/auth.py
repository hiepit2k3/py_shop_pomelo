
from functools import wraps
from flask import request
from exceptions import InvalidCredentialsException

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            print("mjkm")
            raise InvalidCredentialsException("Token is invalid")
    return decorated

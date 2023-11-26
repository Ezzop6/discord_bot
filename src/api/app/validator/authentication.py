from app.config import Config
from flask import request
from functools import wraps
from werkzeug.exceptions import Unauthorized
import hmac

AUTH_HEADER = 'authorization'
AUTH_MODE = 'bearer'


def private_api_route(f):
    """
    Decorator to check valid token provided via HTTP header
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get(AUTH_HEADER, "mode value")
        mode, token = auth_header.split()
        if mode.lower() == AUTH_MODE and validate_token(token):
            return f(*args, **kwargs)
        raise Unauthorized
    return decorated_function


def validate_token(token: str) -> bool:
    return token and hmac.compare_digest(token, Config.TOKEN)

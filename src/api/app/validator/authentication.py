from app.config import Config
from flask import request
from functools import wraps
from werkzeug.exceptions import Unauthorized
import hmac
import logging
from services.logger import logger

AUTH_HEADER = 'authorization'
AUTH_MODE = 'bearer'


def private_api_route(f):
    """
    Decorator to check valid token provided via HTTP header
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get(AUTH_HEADER, "mode value")
        origin = request.headers.get('origin', "origin value")
        logger.log_sync_message(logging.INFO, f"origin: {origin}")
        logger.log_sync_message(logging.INFO, f"auth_header: {auth_header}")
        mode, token = auth_header.split()
        logger.log_sync_message(logging.INFO, f"config token: {Config.TOKEN} - token: {token}")

        if mode.lower() == AUTH_MODE and validate_token(token):
            return f(*args, **kwargs)
        raise Unauthorized
    return decorated_function


def validate_token(token: str) -> bool:
    return token and hmac.compare_digest(token, Config.TOKEN)

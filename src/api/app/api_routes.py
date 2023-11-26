from services.logger import logger
import logging
from flask import request, make_response
from app import app
from app.validator import validate_token, private_api_route

from app.bot_connection import BotConnection
from app.config import Config

from .schemas.api_schema import (
    HealthStatus,
    LoginInput,
    LoginResponse,
    Message,
)
from werkzeug.exceptions import (
    Unauthorized,
)
bot_connection = BotConnection()


@app.get("/status")
@app.output(HealthStatus.Schema)  # type: ignore
@app.doc(
    responses=[200],
    summary="Get status of the service",
    tags=["Health"],
)
def app_status():
    return HealthStatus(status="Hello From API")


@app.get("/bot-status")
@app.output(HealthStatus.Schema)  # type: ignore
@app.doc(
    responses=[200],
    summary="Get status of the bot",
    tags=["Health"],

)
def bot_status():
    bot_status = bot_connection.get_bot_status()
    origin = request.headers.get('Origin')
    logger.log_sync_message(logging.INFO, f'Current origin: {origin} and allowed origins: {Config.ALLOWED_ORIGINS}')
    request_data = request.get_json()
    logger.log_sync_message(logging.INFO, f'Current request data: {request_data}')
    return HealthStatus(status=bot_status)


@app.post("/send-message-to-bot")
@private_api_route
@app.input(Message.Schema)  # type: ignore
@app.doc(
    responses=[200],
    summary="Send message to the bot",
    security='ApiKeyAuth',
    tags=["AUTH"],
)
def send_message_to_bot(message: Message):
    bot_connection.send_message_to_bot(message.message)
    return f'Message sent to bot: {message.message}'


@app.post("/login")
@app.input(LoginInput.Schema)  # type: ignore
@app.output(LoginResponse.Schema)  # type: ignore
@app.doc(
    responses=[200, 401],
    summary="Login route with token",
    tags=["Auth"],
)
def login(login_input: LoginInput):
    if not validate_token(login_input.token):
        raise Unauthorized('Invalid token given')
    return LoginResponse()


@app.after_request
def after_request_func(response):
    origin = request.headers.get('Origin')
    if origin is None:
        origin = '*'

    if request.method == 'GET':
        response = make_response()
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE')
        if origin in Config.ALLOWED_ORIGINS:
            response.headers.add('Access-Control-Allow-Origin', origin)

    else:
        response.headers.add('Access-Control-Allow-Credentials', 'true')

        if origin in Config.ALLOWED_ORIGINS:
            response.headers.add('Access-Control-Allow-Origin', origin)
    logger.log_sync_message(logging.INFO, f'Current origin: {origin} and allowed origins: {Config.ALLOWED_ORIGINS}')
    return response

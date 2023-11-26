from app import app
from app.validator import validate_token
from app.bot_connection import BotConnection
from .schemas.api_schema import (
    HealthStatus,
    LoginInput,
    LoginResponse,
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
    return HealthStatus(status=bot_status)


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

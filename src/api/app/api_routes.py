from app import app
from flask import request, make_response, abort
from app.validator import private_api_route, validate_token

from werkzeug.exceptions import (
    Unauthorized,
)

from .schemas.api_schema import (
    HealthStatus,
    LoginInput,
    LoginResponse,
)


@app.get("/status")
@app.output(HealthStatus.Schema)  # type: ignore
@app.doc(
    responses=[200],
    summary="Get status of the service",
    tags=["Health"],
)
def status():
    return HealthStatus()


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

from marshmallow_dataclass import dataclass


@dataclass
class HealthStatus:
    status: str = "OK"


@dataclass
class LoginInput:
    token: str


@dataclass
class LoginResponse:
    status: int = 200
    message: str = "Success login"


@dataclass
class Message:
    message: str

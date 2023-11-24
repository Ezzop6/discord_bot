from apiflask import APIFlask
from .app_config import Config, ApiConfig


def create_app():
    app = APIFlask(__name__, **ApiConfig)
    app.config.from_object(Config)

    return app


app = create_app()
from app.api_routes import *  # noqa
from .api_error import * # noqa

ErrorResponder()

import os

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(',')


class Config:
    DEBUG: bool = os.getenv("DEBUG") == "True"
    port: int = 5000
    TOKEN: str = os.getenv("API_SECRET_KEY", '')
    BOT_PORT: int = int(os.getenv("INTERNAL_PORT_BOT", "8081"))
    BOT_URL: str = f'http://bot:{BOT_PORT}/'
    SECURITY_SCHEMES = {
        'ApiKeyAuth': {
            'type': 'http',
            'scheme': 'bearer',
        }
    }


ApiConfig = dict(
    title="Marvin Home Assistant API",
    docs_path='/docs',
    spec_path='/docs/openapi.json',
)

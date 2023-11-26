import os


class Config:
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(',')
    external_port: int = int(os.getenv("HOST_DEV_PORT_API", ""))

    if 'localhost' in ALLOWED_ORIGINS:
        ALLOWED_ORIGINS.append(f'http://localhost:{external_port}')

    DEBUG: bool = os.getenv("DEBUG") == "True"
    internal_port: int = 5000
    external_port: int = int(os.getenv("HOST_DEV_PORT_API", ""))
    TOKEN: str = os.getenv("API_SECRET_KEY", '')
    BOT_PORT: int = int(os.getenv("INTERNAL_PORT_BOT", ""))
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

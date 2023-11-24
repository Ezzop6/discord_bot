import os


class Config:
    DEBUG: bool = os.getenv("DEBUG") == "True"
    port: int = 5000
    TOKEN: str = os.getenv("API_SECRET_KEY", '')
    SECURITY_SCHEMES = {
        'ApiKeyAuth': {
            'type': 'http',
            'scheme': 'bearer',
        }
    }


ApiConfig = dict(
    title="AI Link builder demo",
    docs_path='/docs',
    spec_path='/docs/openapi.json',
)

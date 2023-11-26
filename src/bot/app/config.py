from dataclasses import dataclass
import os


PRIVATE_MESSAGE_PREFIX = ['?', '!',]
ANSWER_WORDS = [
    'marwe',
    'trubko',
    'trubka',
]


@dataclass
class AppConfig:
    DEBUG = os.getenv("DEBUG", "False") == "True"
    PORT_API: int = int(os.getenv("INTERNAL_PORT_API", "8080"))
    API_URL: str = f'http://api:{PORT_API}/'
    PORT_BOT: int = int(os.getenv("INTERNAL_PORT_BOT", "8081"))


@dataclass
class BotConfig:
    URL: str = os.getenv("DISCORD_BOT_URL", "")
    name: str = os.getenv("DISCORD_BOT_NAME", "")
    TOKEN: str = os.getenv("DISCORD_BOT_TOKEN", "")
    permission: str = os.getenv("DISCORD_BOT_PERMISSION", "")

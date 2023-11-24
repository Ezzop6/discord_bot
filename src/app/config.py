from dataclasses import dataclass
import os


from dotenv import load_dotenv
load_dotenv()

PRIVATE_MESSAGE_PREFIX = [
    '?', '!',
]
ANSWER_WORDS = [
    'marwe',
    'trubko',
]


@dataclass
class AppConfig:
    debug = os.getenv("DEBUG", "False") == "True"
    open_api_key = os.getenv("OPEN_API_KEY", "")


@dataclass
class BotConfig:
    URL: str = os.getenv("DISCORD_BOT_URL", "")
    name: str = os.getenv("DISCORD_BOT_NAME", "")
    TOKEN: str = os.getenv("DISCORD_BOT_TOKEN", "")
    permission: str = os.getenv("DISCORD_BOT_PERMISSION", "")

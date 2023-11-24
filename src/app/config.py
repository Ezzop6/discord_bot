from dataclasses import dataclass
import os


@dataclass
class BotConfig:
    URL: str = os.getenv("DISCORD_BOT_URL", "")
    name: str = os.getenv("DISCORD_BOT_NAME", "")
    token: str = os.getenv("DISCORD_BOT_TOKEN", "")
    permission: str = os.getenv("DISCORD_BOT_PERMISSION", "")

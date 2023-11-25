from dataclasses import dataclass
import os


@dataclass
class services_config:
    OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY", "")

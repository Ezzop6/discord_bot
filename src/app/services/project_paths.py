import pathlib
from dataclasses import dataclass


@dataclass
class ProjectFolders:
    root = pathlib.Path(__file__).parent.parent.parent.parent
    src = root / 'src'
    app = src / 'app'
    services = app / 'services'
    # logs folders
    logs = root / 'logs'
    bot_log = logs / 'bot'

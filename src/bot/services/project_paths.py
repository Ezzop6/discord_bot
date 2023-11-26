import pathlib
from dataclasses import dataclass
import os


def is_running_in_docker() -> bool:
    if os.path.exists('/.dockerenv'):
        return True

    try:
        with open('/proc/self/cgroup', 'rt') as file:
            if 'docker' in file.read():
                return True
    except Exception:
        pass

    return False


@dataclass
class ProjectFolders:
    if is_running_in_docker():
        root = pathlib.Path(__file__).parent.parent.parent.parent
        src = root / 'code'
    else:
        root = pathlib.Path(__file__).parent.parent.parent
        src = root / 'src'

    bot_app = src / 'app'
    bot_services = bot_app / 'services'
    bot_prompts = bot_services / 'gpt_prompts'

    # logs folders
    logs = root / 'logs'
    bot_log = logs / 'bot'


# @dataclass
# class ProjectFolders:
#     root = pathlib.Path(__file__).parent.parent.parent.parent
#     src = root / 'src'

#     api = src / 'api'
#     bot = src / 'bot'

#     bot_services = bot / 'services'
#     bot_prompts = bot_services / 'gpt_prompts'
#     # logs folders
#     logs = root / 'logs'
#     bot_log = logs / 'bot'
#     api_log = logs / 'api'

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

    app_app = src / 'app'
    app_services = app_app / 'services'

    # logs folders
    logs = root / 'logs'
    api_log = logs / 'api'

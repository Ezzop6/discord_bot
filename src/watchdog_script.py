import time
import pathlib
import subprocess
from dataclasses import dataclass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


@dataclass
class ObservedFile:
    work_dir: pathlib.Path = pathlib.Path(__file__).parent.absolute().parent
    container_name: str = work_dir.name.split("/")[-1]
    bot_path: pathlib.Path = pathlib.Path(__file__).parent.absolute() / "bot"
    api_path: pathlib.Path = pathlib.Path(__file__).parent.absolute() / "api"

    def get_observed_folders(self):
        return [
            self.bot_path,
            self.api_path,
        ]

    def blacklisted_files(self):
        return [
            "__pycache__",
        ]


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        container_name = event.src_path.split("/")
        print(container_name)
        if 'bot' in container_name:
            if any([blacklisted in container_name for blacklisted in ObservedFile().blacklisted_files()]):
                return
            self.restart_docker_container("bot")

    def restart_docker_container(self, container_name):
        try:
            container_name = f"{ObservedFile().container_name}_{container_name}_1"
            subprocess.run(["docker", "restart", container_name], check=True)
            print(f"Restarting container {container_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error restarting container {container_name}: {e}")


if __name__ == "__main__":
    event_handler = MyHandler()
    observers = []

    for folder in ObservedFile().get_observed_folders():
        if folder.is_dir():
            observer = Observer()
            observer.schedule(event_handler, folder, recursive=True)
            observer.start()
            observers.append(observer)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()

    for observer in observers:
        observer.join()

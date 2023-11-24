import logging
import os
from datetime import datetime

from .project_paths import ProjectFolders


class Logger:
    def __init__(self) -> None:
        self.check_folder()
        self.set_logger()

    def set_logger(self) -> None:
        """
        Sets the logger with the log level and the file handler.
        """
        log_level = logging.DEBUG if os.getenv("DEBUG") == "True" \
            else logging.INFO
        self.log = logging.getLogger('Mar-log')
        self.log.setLevel(log_level)
        file_handler = logging.FileHandler(self.log_path)
        file_handler.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        self.log.addHandler(file_handler)

    def check_folder(self) -> None:
        """
        Sets the log folder and sets the log path.
        """
        today = self.get_today()
        self.today = today
        log_folder = ProjectFolders.bot_log
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        log_file = f"Marvin_{today}.log"
        self.log_path = log_folder / log_file

    def log_message(self, level: int, msg: str):
        """
        Logs a message with the given level.
        :param level: logging enum level
        :param msg: The message to log
        """
        if self.today != self.get_today():
            self.check_folder()
            self.set_logger()
        self.log.log(level, msg)

    def get_today(self) -> str:
        return datetime.now().strftime("%Y_%m_%d")


logger = Logger()
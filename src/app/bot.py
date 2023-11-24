import logging

from src.services.logger import logger
from src.services.connection import HTTPSConnectionClient
from src.services.project_paths import ProjectFolders
from .config import BotConfig as CFG


class Bot:
    def __init__(self):
        self.project_folders = ProjectFolders()
        self.client = HTTPSConnectionClient(CFG.URL)


test = Bot()

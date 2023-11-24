from http.client import HTTPSConnection
import logging

from .logger import logger


class HTTPSConnectionClient:
    def __init__(self, host, **kwargs):
        self.connection = HTTPSConnection(host, **kwargs)

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logger.log_message(logging.ERROR, f"Error: {exc_type} {exc_val}")
        self.connection.close()

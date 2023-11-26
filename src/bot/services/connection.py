from http.client import HTTPSConnection, HTTPConnection
import logging

from .logger import logger


class HTTPSConnectionClient:
    def __init__(self, host, **kwargs):
        self.connection = HTTPSConnection(host, **kwargs)

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logger.log_sync_message(logging.ERROR, f"Error: {exc_type} {exc_val}")
        self.connection.close()


class HTTPConnectionClient:
    def __init__(self, host, **kwargs):
        self.connection = HTTPConnection(host, **kwargs)

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logger.log_sync_message(logging.ERROR, f"Error: {exc_type} {exc_val}")
        self.connection.close()

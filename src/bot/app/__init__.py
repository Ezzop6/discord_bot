from .bot import DiscordBot as Bot
from .http_server import DiscordHTTPServer
from .config import AppConfig
import threading


def run_http_server():
    http_server = DiscordHTTPServer(host='bot', port=AppConfig.PORT_BOT)
    http_server_thread = threading.Thread(target=http_server.run)
    http_server_thread.daemon = True
    http_server_thread.start()


def create_bot():
    run_http_server()
    Bot().run_bot()

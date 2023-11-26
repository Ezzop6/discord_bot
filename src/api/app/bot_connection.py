import requests
from app.config import Config


class BotConnection:
    def __init__(self):
        self.bot_url = Config.BOT_URL

    def send_message_to_bot(self, message: str):
        with requests.post(f'{self.bot_url}/send-message', json={'message': message}) as conn:
            data = conn.json()
            return data

    def get_bot_status(self):
        with requests.get(f'{self.bot_url}/status') as conn:
            data = conn.json()
            return data

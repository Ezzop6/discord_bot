import requests
from app.config import Config

conn = requests.get(f'{Config.BOT_URL}/status')
status = conn.json()
print(status)

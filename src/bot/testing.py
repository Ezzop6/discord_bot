import requests
from app.config import AppConfig


conn = requests.get(f'{AppConfig.API_URL}/status')
status = conn.json()
print(status)

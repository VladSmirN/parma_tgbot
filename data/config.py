import os
from pathlib import Path

PORT = 8877
BOT_TOKEN = os.environ["bot_token"]
NGROK_TOKEN = os.environ["NGROK_TOKEN"]
WEBHOOK_PATH = f'/tg/webhooks/bot/{BOT_TOKEN}'

LOGS_BASE_PATH = str(Path(__file__).parent.parent / 'logs')

admins = []

mongo = {
    'hostname':  'mongo',
    'password': 'root',
    'username':  'example',
    'port': 27017,
    'database': 'telegram_bot'
}

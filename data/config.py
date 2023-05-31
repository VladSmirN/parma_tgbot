import os
from pathlib import Path

PORT = 8877
PROD_OR_DEV = os.environ["PROD_OR_DEV"]
BOT_TOKEN = os.environ["bot_token"]
NGROK_TOKEN = os.environ["NGROK_TOKEN"]
WEBHOOK_PATH = f'/tg/webhooks/bot/{BOT_TOKEN}'

LOGS_BASE_PATH = str(Path(__file__).parent.parent / 'logs')

admins = []

if PROD_OR_DEV == 'prod':
    #запуск в докере
    HOSTNAME = 'mongo'
else:
    #запуск на локальной машине
    HOSTNAME = 'localhost'

mongo = {
    'hostname':  HOSTNAME,
    'password': 'root',
    'username':  'example',
    'port': 27017,
    'database': 'english_bot'
}

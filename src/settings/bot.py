
from .django import env


TOKEN_BOT = env.str('TOKEN_BOT')

WEB_SERVER_HOST = env.str("WEB_SERVER_HOST")
WEB_SERVER_PORT = env.int("WEB_SERVER_PORT")
WEBHOOK_HOST = env.str('WEBHOOK_HOST')
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
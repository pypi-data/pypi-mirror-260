import requests

from . import settings, utils

TOKEN = ''


def init(token: str) -> None:
    global TOKEN
    TOKEN = token


def send_message(to: str, msg: str) -> None:
    utils.check_token(TOKEN)
    api_url = settings.TELEGRAM_API_BASE_URL.format(token=TOKEN, method='sendMessage')
    requests.get(api_url, dict(chat_id=to, text=msg, parse_mode='MarkdownV2'))

import json
from .model import ModelSetting
import requests

def send_telegram_message(message):
    api_key = ModelSetting.get('telegram_api_key')
    chat_id = ModelSetting.get('telegram_chat_id')
    if not api_key or not chat_id:
        return
    url = f"https://api.telegram.org/bot{api_key}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(url, data=payload)
	
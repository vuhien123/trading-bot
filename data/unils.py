import requests
from config import DISCORD_WEBHOOK

def send_discord(message):
    data = {
        "content": message
    }
    requests.post(DISCORD_WEBHOOK, json=data)

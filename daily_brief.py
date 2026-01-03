import os
import requests
import random

TELEGRAM_TOKEN = os.getenv("7720152782:AAFr5mbjfmzCxD95IFuDego5Wq7rVZT5z-0")
CHAT_ID = os.getenv("1520967509")

MESSAGES = [
    "🧠 Idée du jour\nLa clarté vient souvent de ce qu’on décide d’arrêter.",
    "💡 Rappel\nCe qui est simple est souvent plus efficace.",
    "❓ Question\nQu’est-ce qui te prend de l’énergie inutilement ?"
]

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    message = random.choice(MESSAGES)
    send_message(message)

import os
import json
import requests
import random
from datetime import datetime, timedelta

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

MESSAGES_FILE = "messages.json"
HISTORY_FILE = "history.json"
MAX_DAYS = 30

def load_json(file_path, default):
    if not os.path.exists(file_path):
        return default
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def clean_history(history):
    cutoff = datetime.utcnow() - timedelta(days=MAX_DAYS)
    return [
        h for h in history
        if datetime.fromisoformat(h["date"]) > cutoff
    ]

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

if __name__ == "__main__":
    messages = load_json(MESSAGES_FILE, [])
    history = load_json(HISTORY_FILE, [])

    history = clean_history(history)
    used_messages = {h["message"] for h in history}

    available_messages = [m for m in messages if m not in used_messages]

    if not available_messages:
        available_messages = messages  # reset après 30 jours

    message = random.choice(available_messages)

    send_message(message)

    history.append({
        "date": datetime.utcnow().isoformat(),
        "message": message
    })

    save_json(HISTORY_FILE, history)

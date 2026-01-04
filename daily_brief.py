import os
import json
import requests
from datetime import datetime, timedelta
import random

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

HISTORY_FILE = "history.json"
MAX_DAYS = 30

MESSAGES = [
    "🧠 Focus\nCe que tu répètes devient ton identité.",
    "💡 Clarté\nLa confusion vient rarement d’un manque d’informations.",
    "📈 Business\nUn système médiocre exécuté chaque jour bat une stratégie parfaite jamais lancée.",
    "🎯 Priorité\nSi tout est important, rien ne l’est.",
    "⚙️ Process\nCe qui n’est pas mesuré dérive.",
    "🧠 Mental\nLa discipline est une forme de respect envers soi-même.",
    "💡 Insight\nArrêter est parfois plus stratégique que continuer.",
    "📈 Levier\nUn petit avantage répété devient énorme avec le temps.",
    "🎯 Décision\nCe que tu repousses aujourd’hui te coûtera demain."
]

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

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
    history = load_history()
    history = clean_history(history)

    used_messages = {h["message"] for h in history}
    available_messages = [m for m in MESSAGES if m not in used_messages]

    if not available_messages:
        available_messages = MESSAGES  # reset propre

    message = random.choice(available_messages)

    send_message(message)

    history.append({
        "date": datetime.utcnow().isoformat(),
        "message": message
    })

    save_history(history)

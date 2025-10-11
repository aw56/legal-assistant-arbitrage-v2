import os
import sys

import requests


def send_telegram_message(message: str):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        raise ValueError("❌ TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не установлены в окружении.")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Ошибка при отправке уведомления: {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ Использование: python notify_telegram.py 'Текст сообщения'")
        sys.exit(1)

    msg = sys.argv[1]
    send_telegram_message(msg)
    print("✅ Уведомление отправлено!")

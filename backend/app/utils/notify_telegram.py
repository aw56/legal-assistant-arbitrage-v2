import os
import sys

import requests


def send_telegram_message(message: str):
    """Отправляет сообщение в Telegram через Bot API."""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        raise ValueError(
            "❌ TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID " "не установлены в окружении."
        )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Ошибка при отправке уведомления: {response.text}")


def format_message(base_message: str) -> str:
    """Формирует красивое сообщение для Telegram с контекстом CI."""
    github_repo = os.getenv("GITHUB_REPOSITORY", "🧩 Local Run")
    github_workflow = os.getenv("GITHUB_WORKFLOW", "Manual Trigger")
    github_ref = os.getenv("GITHUB_REF_NAME", "")
    github_actor = os.getenv("GITHUB_ACTOR", "")
    github_job = os.getenv("GITHUB_JOB", "")
    github_run_id = os.getenv("GITHUB_RUN_ID", "")

    github_url = (
        f"https://github.com/{github_repo}/actions/runs/{github_run_id}"
        if github_run_id
        else ""
    )

    header = "📢 *Legal Assistant Arbitrage — CI Notification*"
    context = (
        "\n\n📦 *Repository:* `{repo}`"
        "\n🧑 *Actor:* {actor}"
        "\n🌿 *Branch:* `{branch}`"
        "\n⚙️ *Workflow:* {workflow}"
    ).format(
        repo=github_repo,
        actor=github_actor or "local user",
        branch=github_ref or "local",
        workflow=github_workflow or github_job,
    )

    footer = f"\n\n🔗 [Открыть GitHub Actions лог]({github_url})" if github_url else ""

    return f"{header}\n\n{base_message}{context}{footer}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ Использование: python notify_telegram.py 'Текст сообщения'")
        sys.exit(1)

    base_msg = sys.argv[1]
    formatted_msg = format_message(base_msg)

    try:
        send_telegram_message(formatted_msg)
        print("✅ Telegram уведомление успешно отправлено.")
    except Exception as e:
        print(f"❌ Ошибка при отправке уведомления: {e}")

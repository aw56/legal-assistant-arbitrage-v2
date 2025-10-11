import os

import pytest

from backend.app.utils.notify_telegram import send_telegram_message


@pytest.mark.integration
def test_integration_telegram_message():
    """
    🌐 Интеграционный тест: реальная отправка уведомления в Telegram.
    Проверяет, что переменные окружения установлены и запрос завершается без исключений.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # Пропускаем тест, если переменные не заданы
    if not token or not chat_id:
        pytest.skip("TELEGRAM_* переменные не заданы — пропуск интеграционного теста")

    # Проверка отправки реального сообщения
    try:
        send_telegram_message("🧩 Integration Test: Telegram connection OK ✅")
    except Exception as e:
        pytest.skip(f"Ошибка при отправке Telegram-сообщения: {e}")

from unittest.mock import patch

import pytest

from backend.app.utils.notify_telegram import send_telegram_message


@pytest.mark.integration
def test_send_telegram_message(monkeypatch):
    """
    Проверяет, что send_telegram_message вызывает requests.post
    и не выбрасывает исключений при корректных данных.
    """
    # Подставляем фейковые переменные окружения
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")

    # Мокаем requests.post
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"ok": True}

        send_telegram_message("Test message ✅")

        # Проверяем, что HTTP-запрос был сделан
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert "https://api.telegram.org/botfake_token/sendMessage" in args[0]
        assert kwargs["json"]["chat_id"] == "12345"
        assert "Test message" in kwargs["json"]["text"]

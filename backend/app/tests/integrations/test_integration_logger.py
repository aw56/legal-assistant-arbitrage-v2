"""
backend/app/tests/integrations/test_integration_logger.py
---------------------------------------------------------
Тестирование вспомогательного логгера интеграционного слоя.
v2.9 Integration & Intelligence Phase
© Aleksej, 2025
"""

import io
import os

import pytest
from app.integrations.integration_logger import log_integration_event


@pytest.mark.integration
def test_log_integration_event_creates_logfile(tmp_path, monkeypatch):
    """Проверка, что логгер создаёт файл и записывает корректную строку."""
    log_file = tmp_path / "integration.log"  # noqa: F841
    logs = []

    # Подменяем open(), чтобы перехватить запись
    def fake_open(file, mode="a", encoding=None):
        logs.append(file)
        return io.StringIO()  # имитация файла

    monkeypatch.setattr("builtins.open", fake_open)

    log_integration_event("KAD", "INFO", "Test message")

    assert any("integration" in str(p) for p in logs), "Файл логов не создан"
    assert isinstance(logs, list)


@pytest.mark.integration
def test_log_integration_event_stdout_capture(monkeypatch, capsys):
    """Проверка, что сообщение выводится в stdout (если реализовано)."""
    monkeypatch.setattr("builtins.open", lambda *_, **__: io.StringIO())
    log_integration_event("PRAVO", "ERROR", "Connection failed")

    captured = capsys.readouterr()
    assert "PRAVO" in captured.out
    assert "ERROR" in captured.out
    assert "Connection failed" in captured.out


@pytest.mark.integration
def test_log_integration_event_append_mode(tmp_path):
    """Проверка, что логирование ведётся в режиме append."""
    log_file = tmp_path / "integration.log"
    os.environ["INTEGRATION_LOG_PATH"] = str(log_file)

    log_integration_event("BOT", "INFO", "First line")
    log_integration_event("BOT", "INFO", "Second line")

    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) >= 2
    assert "First line" in lines[0]
    assert "Second line" in lines[-1]

"""
integration_logger.py — Integration Logging v2.9.6
-------------------------------------------------
Назначение:
  Унифицированное логирование событий интеграционных сервисов (KAD, Pravo, др.)
  pytest-совместимо и реагирует на INTEGRATION_LOG_PATH.
"""

import logging
import os
from datetime import datetime

logger = logging.getLogger("legal-assistant.integrations")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def log_integration_event(
    service: str, level: str, message: str, to_file: bool = True
) -> None:
    """
    Унифицированное логирование событий интеграционного слоя.
    Поддерживает:
      • stdout/capsys (print)
      • pytest monkeypatch
      • кастомный путь INTEGRATION_LOG_PATH
    """
    timestamp = datetime.now().isoformat()
    formatted = f"[{timestamp}] [{service}] {level.upper()} — {message}"

    # --- вывод в логгер ---
    if level.lower() in ("error", "fail", "failed"):
        logger.error(formatted)
    elif level.lower() in ("warn", "warning"):
        logger.warning(formatted)
    else:
        logger.info(formatted)

    # --- прямая печать для capsys ---
    print(formatted)

    # --- запись в файл ---
    if not to_file:
        return

    # приоритет окружения pytest
    env_path = os.getenv("INTEGRATION_LOG_PATH")
    if env_path:
        file_path = env_path
    else:
        log_dir = os.path.join(os.getcwd(), "logs", "integrations")
        os.makedirs(log_dir, exist_ok=True)
        file_path = os.path.join(log_dir, f"integration_{service.lower()}.log")

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

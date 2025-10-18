"""
backend/app/__init__.py
-----------------------
App-level initializer (v2.9 Clean Import Matrix)
Создаёт alias `app.integrations` → `backend.app.integrations`
"""

import importlib
import sys

_real_pkg = "backend.app"

# Загружаем integrations, если есть
try:
    integrations_pkg = importlib.import_module(f"{_real_pkg}.integrations")
    sys.modules["app.integrations"] = integrations_pkg
except ModuleNotFoundError:
    pass

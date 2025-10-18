"""
backend/__init__.py
-------------------
Root package initializer.
Создаёт alias `app → backend.app` для тестов и динамических импортов.
"""

import importlib
import sys

_real_app = importlib.import_module("backend.app")
sys.modules["app"] = _real_app

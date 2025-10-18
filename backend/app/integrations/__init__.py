"""
backend/app/integrations/__init__.py
------------------------------------
Integration Layer Init (v2.9 Clean Import Matrix)
Гарантирует доступность цепочки:
  app.integrations.integration_logger
  app.integrations.base_service
"""

import importlib
import sys

_real_pkg = "backend.app.integrations"

for submod in ("integration_logger", "base_service"):
    try:
        module = importlib.import_module(f"{_real_pkg}.{submod}")
        sys.modules[f"app.integrations.{submod}"] = module
    except ModuleNotFoundError:
        pass

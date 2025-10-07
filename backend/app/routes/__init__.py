# backend/app/routes/__init__.py

import importlib
import pathlib
import pkgutil

# Получаем путь к текущему пакету (routes/)
PACKAGE_DIR = pathlib.Path(__file__).resolve().parent

__all__ = []

# Проходим по всем модулям в папке routes
for _, module_name, is_pkg in pkgutil.iter_modules([str(PACKAGE_DIR)]):
    # Пропускаем __init__.py
    if module_name == "__init__":
        continue

    # Импортируем модуль
    module = importlib.import_module(f"{__package__}.{module_name}")

    # Добавляем в __all__
    __all__.append(module_name)

    # Экспортируем модуль в пространство имён пакета
    globals()[module_name] = module

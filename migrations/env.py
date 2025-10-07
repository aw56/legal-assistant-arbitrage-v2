import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

# === Добавляем корень проекта в PYTHONPATH ===
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from backend.app import models  # noqa: F401, E402
from backend.app.database import Base  # noqa: E402

# Alembic Config
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# Метаданные моделей для автогенерации
target_metadata = Base.metadata


def get_database_url() -> str:
    """Берём DATABASE_URL из окружения."""
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("❌ DATABASE_URL не найден в окружении")
    print(f"📌 Alembic использует DATABASE_URL={url}")
    return url


def run_migrations_offline() -> None:
    """Запуск миграций в оффлайн-режиме (генерация SQL)."""
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в онлайн-режиме (через подключение к БД)."""
    url = get_database_url()
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

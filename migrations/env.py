import os
import sys
from logging.config import fileConfig
from urllib.parse import quote_plus

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

# --- Загружаем .env ---
load_dotenv(".env")

# --- Alembic config ---
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Подключение к БД ---
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASS = quote_plus(os.getenv("POSTGRES_PASSWORD", "admin"))
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "legal_assistant_db")

SQLALCHEMY_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# 👉 Записываем URL напрямую в attributes, а не через set_main_option
config.attributes["sqlalchemy.url"] = SQLALCHEMY_URL

# --- Импорт моделей ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.app.database import Base  # noqa

target_metadata = Base.metadata


def run_migrations_offline():
    """Запуск миграций без подключения к БД (генерация SQL)."""
    url = config.attributes.get("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Запуск миграций с подключением к реальной БД."""
    connectable = engine_from_config(
        {"sqlalchemy.url": config.attributes.get("sqlalchemy.url")},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

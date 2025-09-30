import logging
import os

from alembic.config import Config
from alembic.script import ScriptDirectory
from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from backend.app.database import SessionLocal

router = APIRouter()
logger = logging.getLogger("health")

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
APP_ENV = os.getenv("APP_ENV", "development")
USE_SQLITE = os.getenv("USE_SQLITE") == "1"


def get_alembic_status():
    """
    Проверка, актуальны ли миграции Alembic.
    Сравнивает ревизию в БД с последней ревизией в папке migrations.
    """
    try:
        alembic_cfg = Config("alembic.ini")
        script = ScriptDirectory.from_config(alembic_cfg)

        db = SessionLocal()
        result = db.execute(text("SELECT version_num FROM alembic_version"))
        db.close()

        current_rev = result.scalar()
        head_rev = script.get_current_head()

        if current_rev == head_rev:
            return "up-to-date"
        else:
            return f"outdated (db={current_rev}, head={head_rev})"
    except Exception as e:
        logger.error(f"Ошибка проверки Alembic: {e}")
        return f"error: {str(e)}"


@router.get("/health")
def health_check():
    """
    Health-check эндпоинт:
    - статус API
    - версия приложения
    - окружение (development/production)
    - тип БД (SQLite/PostgreSQL)
    - подключение к БД
    - состояние миграций Alembic
    """
    status = {
        "status": "ok",
        "version": APP_VERSION,
        "env": APP_ENV,
        "db_type": "SQLite" if USE_SQLITE else "PostgreSQL",
    }

    # Проверка подключения к БД
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        status["db_status"] = "connected"
    except SQLAlchemyError as e:
        logger.error(f"❌ Ошибка подключения к БД: {e}")
        status["db_status"] = "error"
        status["status"] = "error"

    # Проверка состояния миграций (только если база доступна и PostgreSQL)
    if status.get("db_status") == "connected" and not USE_SQLITE:
        status["alembic"] = get_alembic_status()

    return status

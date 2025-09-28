import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI

from backend.app.database import Base, engine
from backend.app.routes import decisions, health, laws, users

# Загружаем .env
load_dotenv()

# Логирование
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Проверяем режим БД
use_sqlite = os.getenv("USE_SQLITE") == "1"
if use_sqlite:
    logger.info("✅ Используется SQLite (локальная разработка)")
else:
    logger.info("✅ Используется PostgreSQL (docker/prod)")

# Создаём таблицы
Base.metadata.create_all(bind=engine)

# FastAPI приложение
app = FastAPI(title="Legal Assistant Arbitrage API")

# Подключаем роуты
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(laws.router, prefix="/api/laws", tags=["laws"])
app.include_router(decisions.router, prefix="/api/decisions", tags=["decisions"])

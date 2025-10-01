import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI

from backend.app.database import Base, engine
from backend.app.routes import auth, decisions, health, laws, users

# === Загружаем .env ===
load_dotenv()

# === Логирование ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("legal-assistant")

# === Проверяем режим работы БД ===
USE_SQLITE = os.getenv("USE_SQLITE") == "1"
if USE_SQLITE:
    logger.info("✅ Используется SQLite (локальная разработка)")
    # В dev-режиме создаём таблицы автоматически
    Base.metadata.create_all(bind=engine)
else:
    logger.info("✅ Используется PostgreSQL (docker/prod)")
    # В prod-режиме таблицы создаются миграциями Alembic

# === FastAPI приложение ===
app = FastAPI(
    title="⚖️ Legal Assistant Arbitrage API",
    version="1.0.0",
    description=(
        "API для цифрового помощника юриста по арбитражным делам.\n\n"
        "📌 Доступные модули: пользователи, законы, судебные решения, "
        "авторизация, health-check.\n"
        "🚀 Полная документация доступна в `/docs` (Swagger) или `/redoc`."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)


# === Корневой эндпоинт ===
@app.get("/", tags=["root"])
def root():
    return {
        "message": "⚖️ Добро пожаловать в Legal Assistant Arbitrage API",
        "docs": "/docs",
        "health": "/api/health",
        "auth": "/api/auth",
    }


# === Подключаем роуты ===
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(auth.router)  # 🔑 авторизация (login, register, me)
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(laws.router, prefix="/api/laws", tags=["laws"])
app.include_router(decisions.router, prefix="/api/decisions", tags=["decisions"])

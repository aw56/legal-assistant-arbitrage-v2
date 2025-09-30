import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI

from backend.app.database import Base, engine
from backend.app.routes import decisions, health, laws, users

# Загружаем .env
load_dotenv()

# Логирование
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("legal-assistant")

# Проверяем режим работы БД
USE_SQLITE = os.getenv("USE_SQLITE") == "1"
if USE_SQLITE:
    logger.info("✅ Используется SQLite (локальная разработка)")
    Base.metadata.create_all(bind=engine)  # только для dev
else:
    logger.info("✅ Используется PostgreSQL (docker/prod)")
    # В продакшене таблицы создаются через Alembic миграции

# FastAPI приложение
app = FastAPI(
    title="Legal Assistant Arbitrage API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# Встроенный health-check
@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


# Подключаем роуты
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(laws.router, prefix="/api/laws", tags=["laws"])
app.include_router(decisions.router, prefix="/api/decisions", tags=["decisions"])

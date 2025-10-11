import importlib
import logging
import os
import pathlib
import pkgutil
import subprocess

from dotenv import load_dotenv
from fastapi import FastAPI

# === Загружаем .env ===
load_dotenv()

# === Логирование ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("legal-assistant")

# === Определяем режим работы базы ===
USE_SQLITE = os.getenv("USE_SQLITE") == "1"
if USE_SQLITE:
    logger.info("✅ Используется SQLite (локальная разработка)")
    from backend.app.database import Base, engine

    Base.metadata.create_all(bind=engine)
else:
    logger.info("✅ Используется PostgreSQL (docker/prod)")
    # В продакшене структура управляется через Alembic миграции

# === Инициализация FastAPI ===
app = FastAPI(
    title="⚖️ Legal Assistant Arbitrage API",
    version="1.1.0",
    description=(
        "API для цифрового помощника юриста по арбитражным делам.\n\n"
        "📚 Модули: пользователи, законы, судебные решения, авторизация, health-check.\n"
        "🚀 Документация: `/docs` (Swagger) или `/redoc`."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)


# === Корневой эндпоинт ===
@app.get("/", tags=["root"])
def root():
    """Базовая точка API."""
    return {
        "message": "⚖️ Добро пожаловать в Legal Assistant Arbitrage API",
        "docs": "/docs",
        "health": "/api/health",
        "auth": "/api/auth",
        "reset": "/api/reset",
    }


# === Автоматическое подключение всех роутов ===
def register_routes(app: FastAPI):
    routes_pkg = "backend.app.routes"
    package_dir = pathlib.Path(__file__).resolve().parent / "routes"

    for _, module_name, _ in pkgutil.iter_modules([str(package_dir)]):
        if module_name == "__init__":
            continue

        module = importlib.import_module(f"{routes_pkg}.{module_name}")
        router = getattr(module, "router", None)
        if router:
            # Индивидуальные префиксы
            if module_name == "auth":
                prefix, tags = "/api/auth", ["auth"]
            elif module_name == "health":
                prefix, tags = "/api", ["health"]
            elif module_name == "docs":
                prefix, tags = "/api/docs", ["docs"]
            elif module_name == "reset":
                prefix, tags = "/api", ["system"]
            else:
                prefix, tags = f"/api/{module_name}", [module_name]

            app.include_router(router, prefix=prefix, tags=tags)
            logger.info(f"✅ Роут {module_name} подключен (prefix={prefix})")


# === Подключаем роуты ===
register_routes(app)

# === Импорт отдельных критичных маршрутов ===
from backend.app.routes import docs, reset

app.include_router(docs.router)
app.include_router(reset.router)

logger.info("✅ Роуты docs и reset подключены.")


# === Расширенная команда полного сброса БД ===
@app.post("/api/reset/full", tags=["system"])
def reset_full():
    """
    ⚙️ Полный пересоздание БД (Alembic + миграции)
    Используется в CI/CD и для полного восстановления тестовой среды.
    """
    try:
        logger.info("🧨 Запуск полного ресета базы...")
        subprocess.run(["alembic", "downgrade", "base"], check=False)
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        logger.info("✅ Alembic пересоздал схему.")
        return {"status": "full reset done ✅"}
    except Exception as e:
        logger.error(f"Ошибка при полном сбросе: {e}")
        return {"error": str(e)}


# === Финальный лог ===
logger.info("🚀 Legal Assistant Arbitrage API успешно запущен.")

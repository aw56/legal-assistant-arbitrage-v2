import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Загружаем переменные окружения (.env)
load_dotenv(".env")

# --- Переменные подключения ---
DB_USER = quote_plus(os.getenv("POSTGRES_USER", "admin"))
DB_PASS = quote_plus(os.getenv("POSTGRES_PASSWORD", "admin"))
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "legal_assistant_db")

# --- Формируем строку подключения ---
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# --- База декларативных моделей ---
Base = declarative_base()

# --- Создаём движок ---
engine = create_engine(DATABASE_URL, future=True, echo=False)

# --- SessionLocal для зависимостей ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Dependency для FastAPI ---
def get_db():
    """Зависимость для получения сессии БД."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

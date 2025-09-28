import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

# Загружаем переменные окружения
load_dotenv()

# Логирование
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

Base = declarative_base()


def build_postgres_url() -> URL:
    """Формируем DSN для PostgreSQL"""
    return URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("POSTGRES_USER", "admin"),
        password=os.getenv("POSTGRES_PASSWORD", "admin"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        database=os.getenv("POSTGRES_DB", "legal_assistant_db"),
    )


def get_sqlalchemy_url() -> str:
    """Определяем URL для SQLAlchemy (SQLite или Postgres)"""
    if os.getenv("USE_SQLITE") == "1":
        db_path = "sqlite:///./test.db"
        logger.info(f"🔗 Подключаемся к SQLite: {db_path}")
        return db_path
    else:
        postgres_url = str(build_postgres_url())
        logger.info(f"🔗 Подключаемся к PostgreSQL: {postgres_url}")
        return postgres_url


SQLALCHEMY_DATABASE_URL = get_sqlalchemy_url()

# Подключение движка
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=(
        {"check_same_thread": False}
        if SQLALCHEMY_DATABASE_URL.startswith("sqlite")
        else {}
    ),
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def get_db():
    """Создаём сессию для работы с БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

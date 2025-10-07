import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import models
from backend.app.core.security import get_password_hash
from backend.app.database import Base, get_db
from backend.app.main import app

# === Тестовая БД (SQLite in-memory) ===
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# === Создание/удаление таблиц один раз на сессию ===
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# === Сессия БД для каждого теста ===
@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


# === FastAPI TestClient c подменой get_db ===
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


# === Фикстура: тестовый пользователь admin ===
@pytest.fixture(scope="function")
def test_user(db_session):
    user = models.User(
        username="admin",
        password=get_password_hash("admin123"),
        role=models.UserRole.admin,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.database import Base, engine


@pytest.fixture(scope="function", autouse=True)
def reset_db():
    """
    Фикстура: перед каждым тестом пересоздаёт таблицы в SQLite.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """
    Фикстура для TestClient.
    """
    with TestClient(app) as c:
        yield c

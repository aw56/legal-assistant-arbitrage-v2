import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import models, schemas
from backend.app.database import Base
from backend.app.services import users as user_service


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


def test_create_user(db_session):
    user_in = schemas.UserCreate(
        username="testuser", password="123", role=schemas.UserRole.client
    )
    user = user_service.create_user(db_session, user_in)
    assert user.id is not None
    assert user.username == "testuser"


def test_update_user(db_session):
    user_in = schemas.UserCreate(
        username="user1", password="pwd", role=schemas.UserRole.lawyer
    )
    user = user_service.create_user(db_session, user_in)
    update_data = schemas.UserUpdate(username="updateduser")
    updated_user = user_service.update_user(db_session, user.id, update_data)
    assert updated_user.username == "updateduser"


def test_delete_user(db_session):
    user_in = schemas.UserCreate(
        username="user2", password="pwd", role=schemas.UserRole.client
    )
    user = user_service.create_user(db_session, user_in)
    user_service.delete_user(db_session, user.id)
    assert db_session.query(models.User).filter_by(id=user.id).first() is None

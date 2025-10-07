import pytest
from sqlalchemy.orm import Session

from backend.app import models, schemas
from backend.app.services import users


def test_create_user(db_session: Session):
    user_in = schemas.UserCreate(
        username="user1",
        password="pwd123",
        role=schemas.UserRole.lawyer,  # ✅ теперь это доступно
    )
    user = users.create_user(db_session, user_in)
    assert user.id is not None
    assert user.username == "user1"
    assert user.role == schemas.UserRole.lawyer


def test_read_users(db_session: Session):
    user_in = schemas.UserCreate(
        username="user2",
        password="pwd123",
        role=schemas.UserRole.user,
    )
    users.create_user(db_session, user_in)

    result = users.get_users(db_session)
    assert any(u.username == "user2" for u in result)


def test_update_user(db_session: Session):
    user_in = schemas.UserCreate(
        username="user3",
        password="pwd123",
        role=schemas.UserRole.lawyer,
    )
    user = users.create_user(db_session, user_in)

    update_in = schemas.UserUpdate(username="updated_user3")
    updated_user = users.update_user(db_session, user.id, update_in)

    assert updated_user.username == "updated_user3"


def test_delete_user(db_session: Session):
    user_in = schemas.UserCreate(
        username="user4",
        password="pwd123",
        role=schemas.UserRole.user,
    )
    user = users.create_user(db_session, user_in)

    users.delete_user(db_session, user.id)
    result = users.get_users(db_session)
    assert all(u.id != user.id for u in result)

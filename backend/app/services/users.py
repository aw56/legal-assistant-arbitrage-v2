import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.app import models, schemas
from backend.app.core.security import get_password_hash

logger = logging.getLogger(__name__)


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    logger.info("Создание пользователя: %s", user.username)

    # Проверяем уникальность username
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(
            status_code=400, detail="❌ Пользователь с таким именем уже существует"
        )

    # Проверяем уникальность email
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(
            status_code=400, detail="❌ Пользователь с таким email уже существует"
        )

    # Хешируем пароль
    hashed_password = get_password_hash(user.password)

    # Создаём пользователя
    new_user = models.User(
        username=user.username,
        email=user.email,
        role=user.role,
        password_hash=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session):
    return db.query(models.User).all()


def get_user(db: Session, user_id: int) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="❌ Пользователь не найден")
    return user


def update_user(
    db: Session, user_id: int, user_update: schemas.UserUpdate
) -> models.User:
    user = get_user(db, user_id)
    logger.info("Обновление пользователя ID=%s", user_id)
    for key, value in user_update.model_dump(exclude_unset=True).items():
        if key == "password" and value:
            setattr(user, "password_hash", get_password_hash(value))
        else:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> None:
    user = get_user(db, user_id)
    logger.info("Удаление пользователя ID=%s", user_id)
    db.delete(user)
    db.commit()

import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.app import models, schemas

logger = logging.getLogger(__name__)


def create_user(db: Session, user: schemas.user.UserCreate) -> models.User:
    logger.info("Создание пользователя: %s", user.username)
    db_user = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if db_user:
        raise HTTPException(
            status_code=400, detail="❌ Пользователь с таким именем уже существует"
        )

    new_user = models.User(
        username=user.username, password=user.password, role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session):
    return db.query(models.User).all()


def get_user(db: Session, user_id: int) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="❌ Пользователь не найден")
    return user


def update_user(
    db: Session, user_id: int, user_update: schemas.user.UserUpdate
) -> models.User:
    user = get_user(db, user_id)
    logger.info("Обновление пользователя ID=%s", user_id)
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    logger.info("Удаление пользователя ID=%s", user_id)
    db.delete(user)
    db.commit()
    return {"status": "✅ Пользователь удалён"}

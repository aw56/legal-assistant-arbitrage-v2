from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app import models, schemas
from backend.app.database import get_db

router = APIRouter()


# 🔹 Создать пользователя
@router.post("/", response_model=schemas.user.User)
def create_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
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


# 🔹 Получить всех пользователей
@router.get("/", response_model=List[schemas.user.User])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# 🔹 Получить пользователя по ID
@router.get("/{user_id}", response_model=schemas.user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="❌ Пользователь не найден")
    return user


# 🔹 Обновить пользователя (частично)
@router.patch("/{user_id}", response_model=schemas.user.User)
def update_user(
    user_id: int, user_update: schemas.user.UserUpdate, db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="❌ Пользователь не найден")

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


# 🔹 Удалить пользователя
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="❌ Пользователь не найден")

    db.delete(user)
    db.commit()
    return {"status": "✅ Пользователь удалён"}

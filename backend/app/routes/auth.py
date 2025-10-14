from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app import models, schemas
from backend.app.core.security import (create_access_token, get_current_user,
                                       verify_password)
from backend.app.database import get_db
from backend.app.services import users as user_service

router = APIRouter()


# --- Register ---
@router.post("/register", response_model=schemas.UserRead)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя
    """
    existing = (
        db.query(models.User).filter(models.User.username == user_in.username).first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")

    user = user_service.create_user(db, user_in)
    return user


# --- Login ---
@router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Логин пользователя и получение JWT токена
    """
    user = (
        db.query(models.User).filter(models.User.username == form_data.username).first()
    )
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


# --- Me ---
@router.get("/me", response_model=schemas.UserRead)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Получить информацию о текущем пользователе
    """
    return current_user

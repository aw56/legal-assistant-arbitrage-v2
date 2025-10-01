from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app import schemas
from backend.app.database import get_db
from backend.app.services import users as user_service

router = APIRouter(tags=["users"])


@router.post("/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)


@router.get("/", response_model=list[schemas.UserRead])
def read_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)


@router.get("/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user(db, user_id)


@router.put("/{user_id}", response_model=schemas.UserRead)
def update_user(
    user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)
):
    return user_service.update_user(db, user_id, user_update)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db, user_id)

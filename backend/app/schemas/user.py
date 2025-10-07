from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    admin = "admin"
    lawyer = "lawyer"
    user = "user"
    client = "client"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.user


class UserCreate(UserBase):
    password: str  # ✅ при регистрации получаем пароль в открытом виде


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    password: Optional[str] = None


class UserRead(UserBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


__all__ = [
    "UserRole",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserRead",
    "UserLogin",
    "Token",
]

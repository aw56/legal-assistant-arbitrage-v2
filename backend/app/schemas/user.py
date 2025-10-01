from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class UserRole(str, Enum):
    admin = "admin"
    lawyer = "lawyer"
    client = "client"


class UserBase(BaseModel):
    username: str
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: str | None = None
    role: UserRole | None = None
    password: str | None = None

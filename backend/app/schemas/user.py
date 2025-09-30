from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, constr


# 🔹 Базовая схема (для отображения)
class UserBase(BaseModel):
    username: str
    role: Literal["admin", "lawyer", "client"] = "client"


# 🔹 Для создания пользователя
class UserCreate(UserBase):
    password: constr(min_length=6, max_length=100)


# 🔹 Для обновления пользователя (частичное изменение)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[constr(min_length=6, max_length=100)] = None
    role: Optional[Literal["admin", "lawyer", "client"]] = None


# 🔹 Для возврата пользователю
class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

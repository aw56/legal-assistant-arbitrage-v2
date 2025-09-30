from typing import Optional

from pydantic import BaseModel, ConfigDict


# 🔹 Базовая схема
class LawBase(BaseModel):
    code: str
    article: str
    title: str


# 🔹 Создание
class LawCreate(LawBase):
    pass


# 🔹 Обновление (частичное)
class LawUpdate(BaseModel):
    code: Optional[str] = None
    article: Optional[str] = None
    title: Optional[str] = None


# 🔹 Возврат
class Law(LawBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

from typing import Optional

from pydantic import BaseModel, ConfigDict


# 🔹 Базовая схема
class DecisionBase(BaseModel):
    case_number: str
    court: str
    summary: Optional[str] = None


# 🔹 Создание
class DecisionCreate(DecisionBase):
    pass


# 🔹 Обновление (частичное)
class DecisionUpdate(BaseModel):
    case_number: Optional[str] = None
    court: Optional[str] = None
    summary: Optional[str] = None


# 🔹 Возврат
class Decision(DecisionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

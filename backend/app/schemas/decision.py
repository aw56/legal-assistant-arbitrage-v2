from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DecisionBase(BaseModel):
    case_number: str
    court: str | None = None
    summary: str | None = None


class DecisionCreate(DecisionBase):
    date_decided: datetime | None = None  # ✅ datetime вместо date
    law_id: int | None = None
    user_id: int | None = None


class DecisionUpdate(BaseModel):
    court: str | None = None
    summary: str | None = None
    date_decided: datetime | None = None  # ✅ datetime вместо date
    law_id: int | None = None


class Decision(DecisionBase):
    id: int
    date_decided: datetime | None = None  # ✅ datetime вместо date
    law_id: int | None = None
    user_id: int | None = None
    created_at: datetime
    updated_at: datetime | None = None  # ✅ сделаем опциональным

    model_config = ConfigDict(from_attributes=True)

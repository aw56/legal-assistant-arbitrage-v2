from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class DecisionBase(BaseModel):
    case_number: str
    court: str
    summary: str | None = None


class DecisionCreate(DecisionBase):
    date_decided: date | None = None


class Decision(DecisionBase):
    id: int
    date_decided: date | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DecisionUpdate(BaseModel):
    court: str | None = None
    summary: str | None = None
    date_decided: date | None = None

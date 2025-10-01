from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LawBase(BaseModel):
    code: str
    article: str
    title: str


class LawCreate(LawBase):
    text: str | None = None


class Law(LawBase):
    id: int
    text: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LawUpdate(BaseModel):
    title: str | None = None
    text: str | None = None

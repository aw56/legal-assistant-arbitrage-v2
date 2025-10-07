from pydantic import BaseModel, ConfigDict


class LawBase(BaseModel):
    code: str
    article: str
    title: str


class LawCreate(LawBase):
    description: str | None = None


class LawUpdate(BaseModel):
    # ✅ все поля — опциональные, чтобы можно было менять частично
    code: str | None = None
    article: str | None = None
    title: str | None = None
    description: str | None = None


class Law(LawBase):
    id: int
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)

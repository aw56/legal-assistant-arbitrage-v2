from pydantic import BaseModel, ConfigDict

class LawBase(BaseModel):
    code: str
    article: str
    title: str

class LawCreate(LawBase):
    pass

class Law(LawBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

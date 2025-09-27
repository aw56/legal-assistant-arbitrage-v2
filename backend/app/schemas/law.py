from pydantic import BaseModel

class LawBase(BaseModel):
    code: str
    article: str
    title: str

class LawCreate(LawBase):
    pass

class LawRead(LawBase):
    id: int

    class Config:
        from_attributes = True

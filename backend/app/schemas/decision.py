from pydantic import BaseModel

class DecisionBase(BaseModel):
    case_number: str
    court: str
    summary: str | None = None

class DecisionCreate(DecisionBase):
    pass

class DecisionRead(DecisionBase):
    id: int

    class Config:
        from_attributes = True

from pydantic import BaseModel, ConfigDict

class DecisionBase(BaseModel):
    case_number: str
    court: str
    summary: str

class DecisionCreate(DecisionBase):
    pass

class Decision(DecisionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

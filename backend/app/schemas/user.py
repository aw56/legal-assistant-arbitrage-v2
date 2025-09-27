from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    role: str = "client"

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

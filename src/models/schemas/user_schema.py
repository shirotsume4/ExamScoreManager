from pydantic import BaseModel

class UserBase(BaseModel):
    """Base User scheme"""
    username: str

class UserCreate(UserBase):
    """Input"""
    password: str

class User(UserBase):
    """Output"""
    id: int

    class Config:
        orm_mode = True
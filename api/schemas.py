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

class TokenBase(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class ExamScoreBase(BaseModel):
    """Base ExamScore scheme"""
    examtitle: str
    math_score: int
    english_score: int
    
class ExamScoreCreate(ExamScoreBase):
    user_id: int
    
class ExamScore(ExamScoreBase):
    id: int
    
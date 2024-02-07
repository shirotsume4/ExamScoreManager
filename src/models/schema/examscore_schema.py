from pydantic import BaseModel


class ExamScoreBase(BaseModel):
    """Base ExamScore scheme"""

    examtitle: str
    math_score: int
    english_score: int


class ExamScoreCreate(ExamScoreBase):
    pass


class ExamScore(ExamScoreBase):
    user_id: int
    id: int

    class Config:
        orm_mode = True

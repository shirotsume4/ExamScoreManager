from pydantic import BaseModel


class ExamScoreBase(BaseModel):
    """Base ExamScore scheme"""

    examtitle: str
    math_score: int
    english_score: int


class ExamScoreCreate(ExamScoreBase):
    user_id: int


class ExamScore(ExamScoreBase):
    id: int

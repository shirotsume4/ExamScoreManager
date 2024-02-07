from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.dbengine import Base


class ExamScore(Base):
    __tablename__ = "examscore"

    id = Column(Integer, primary_key=True, index=True)
    examtitle = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    math_score = Column(Integer, index=True)
    english_score = Column(Integer, index=True)
    user = relationship("User", back_populates="examscores")

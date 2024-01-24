from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from DB import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String)
    username = Column(String,index=True)
    examscores = relationship("ExamScore", back_populates="user")

class ExamScore(Base):
    __tablename__ = "examscore"

    id = Column(Integer, primary_key=True, index=True)
    examtitle = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    math_score = Column(Integer, index=True)
    english_score = Column(Integer, index=True)
    
    user = relationship("User", back_populates="examscores")

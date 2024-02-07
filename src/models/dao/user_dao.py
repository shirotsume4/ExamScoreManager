from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from models.dao.DB import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String)
    username = Column(String,index=True)
    examscores = relationship("ExamScore", back_populates="user")
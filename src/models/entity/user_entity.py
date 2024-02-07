from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.dbengine.dbengine import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String)
    username = Column(String, index=True)
    examscores = relationship("ExamScore", back_populates="user")

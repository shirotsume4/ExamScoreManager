from hashlib import sha256 as hash_func

from sqlalchemy.orm import Session

import models.schema.user_schema as schemas
from models.entity.user_entity import User


def get_user_by_username_query(db: Session, username: str):
    """get user by username"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_id_query(db: Session, id: int):
    """get user by id"""
    return db.query(User).filter(User.id == id).first()


def get_all_user_query(db: Session):
    """get all user"""
    return db.query(User).all()


def create_user_query(db: Session, user: schemas.UserCreate):
    """create user by username and password"""
    hashed_password = hash_func(user.password.encode()).hexdigest()
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

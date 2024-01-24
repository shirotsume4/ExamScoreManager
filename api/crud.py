from sqlalchemy.orm import Session
from hashlib import md5 as hash_func
import api.models as models, api.schemas as schemas

def get_user_by_username_query(db: Session, username: str):
    """get user by username"""
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id_query(db: Session, id: int):
    """get user by id"""
    return db.query(models.User).filter(models.User.id == id).first()

def get_all_user_query(db: Session):
    """get all user"""
    return db.query(models.User).all()

def create_user_query(db: Session, user: schemas.UserCreate):
    """create user by username and password"""
    hashed_password = hash_func(user.password.encode()).hexdigest()
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
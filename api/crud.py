from sqlalchemy.orm import Session
from hashlib import md5 as hash_func
import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

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
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
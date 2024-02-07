import models.schema.user_schema as user_schema
from fastapi import Depends, HTTPException, APIRouter
from hashlib import sha256 as hash_func
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.dbengine.dbengine import Base, SessionLocal, engine
from models.dbengine.get_db import get_db
from usecases.user_usecase import (
    create_user_query,
    get_all_user_query,
    get_user_by_id_query,
    get_user_by_username_query
)
router = APIRouter()
@router.post("/token", tags=["users"])
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_dict = get_user_by_username_query(db=db, username=user.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = hash_func(user.password.encode()).hexdigest()
    if not hashed_password == user_dict.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user_dict.id, "token_type": "bearer"}

@router.post("/users/", tags=["users"], response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username_query(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Same username found")
    return create_user_query(db=db, user=user)


@router.get("/users/all", tags=["users"])
def get_all_users(db: Session = Depends(get_db)):
    db_users = get_all_user_query(db=db)
    return db_users


@router.get("/users/{id}", tags=["users"])
def get_user_by_id(id, db: Session = Depends(get_db)):
    db_user = get_user_by_id_query(db=db, id=id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User Not Found")
    return db_user


@router.get("/users/", tags=["users"])
def get_user_by_name(name: str, db: Session = Depends(get_db)):
    db_user = get_user_by_username_query(db=db, username=name)
    if not db_user:
        raise HTTPException(status_code=400, detail="User Not Found")
    return db_user

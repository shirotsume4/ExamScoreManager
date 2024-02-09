from hashlib import sha256 as hash_func

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models.schema.user_schema as user_schema
from db.get_db import get_db
from usecases.user_usecase import (
    create_user_query,
    get_all_user_query,
    get_user_by_id_query,
    get_user_by_username_query
)

router = APIRouter()

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
def get_user_by_name(username: str, db: Session = Depends(get_db)):
    db_user = get_user_by_username_query(db=db, username=username)
    if not db_user:
        raise HTTPException(status_code=400, detail="User Not Found")
    return db_user

from hashlib import sha256 as hash_func

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.get_db import get_db
from usecases.user_usecase import get_user_by_username_query

router = APIRouter()


@router.post("/login", tags=["login"])
def token(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_dict = get_user_by_username_query(db=db, username=user.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = hash_func(user.password.encode()).hexdigest()
    if not hashed_password == user_dict.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user_dict.id, "token_type": "bearer"}

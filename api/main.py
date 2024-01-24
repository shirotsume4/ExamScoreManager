import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import sys
import os
import models
import schemas as schemas
from crud import (
    get_all_user_query,
    get_user_by_id_query,
    get_user_by_username_query,
    create_user_query
)
from auth_api import * 
from DB import engine, Base, SessionLocal
# table作成
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Dependency
def get_db():
    try:
        db = SessionLocal() # sessionを生成
        yield db
    finally:
        db.close()
    db.close()

@app.post("/token", response_model=schemas.TokenBase)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username_query(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Same username found")
    return create_user_query(db=db, user=user)

@app.get("/users/")
def get_all_users(db:Session = Depends(get_db)):
    db_users = get_all_user_query(db=db)
    return db_users

@app.get("/users/{id}")
def get_user_by_id(id, db:Session = Depends(get_db)):
    db_user = get_user_by_id_query(db=db,id=id)
    if not db_user:
        return HTTPException(status_code=400, detail="User Not Found")
    return db_user

if __name__ == "__main__":
    uvicorn.run(app)
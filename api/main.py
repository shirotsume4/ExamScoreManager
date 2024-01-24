import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import sys
import os
import api.models as models
import api.schemas as schemas
from api.crud import (
    get_all_user_query,
    get_user_by_id_query,
    get_user_by_username_query,
    create_user_query
)
from api.DB import engine, Base, SessionLocal
# table作成
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    try:
        db = SessionLocal() # sessionを生成
        yield db
    finally:
        db.close()
    db.close()

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
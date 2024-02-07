import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from hashlib import sha256 as hash_func
from relpath import add_import_path
add_import_path("../")  # ここで、importしたいツールの場所を相対参照で指定
from services.user_service import (
    get_all_user_query,
    get_user_by_id_query,
    get_user_by_username_query,
    create_user_query
)
from models.dao.dbengine import Base, engine,SessionLocal
import models.schemas.examscore_schema as examscore_schema
import models.schemas.user_schema as user_schema
# table作成
Base.metadata.create_all(bind=engine)
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

@app.post("/token")
def login(user: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user_dict = get_user_by_username_query(db=db, username=user.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = hash_func(user.password.encode()).hexdigest()
    if not hashed_password == user_dict.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user_dict.id, "token_type": "bearer"}

@app.post("/users/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
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
        raise HTTPException(status_code=400, detail="User Not Found")
    return db_user

@app.get("/users/")
def get_user_by_name(name, db:Session = Depends(get_db)):
    db_user = get_user_by_username_query(db=db,username=name)
    if not db_user:
        raise HTTPException(status_code=400, detail="User Not Found")
    return db_user

if __name__ == "__main__":
    uvicorn.run(app)
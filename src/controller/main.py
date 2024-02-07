import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from relpath import add_import_path
add_import_path("../")  # ここで、importしたいツールの場所を相対参照で指定
from services.user_service import (
    get_all_user_query,
    get_user_by_id_query,
    get_user_by_username_query,
    create_user_query
)
from models.dao.DB import Base, engine,SessionLocal
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

@app.get("/items/")
def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

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
        return HTTPException(status_code=400, detail="User Not Found")
    return db_user

if __name__ == "__main__":
    uvicorn.run(app)
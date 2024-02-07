from hashlib import sha256 as hash_func

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models.schema.examscore_schema as exam_schema
import models.schema.user_schema as user_schema
from models.dao.dbengine import Base, SessionLocal, engine
from services.examscore_service import (
    create_exam_query,
    get_examscore_by_title_query
)
from services.user_service import (
    create_user_query,
    get_all_user_query,
    get_user_by_id_query,
    get_user_by_username_query
)

# table作成
Base.metadata.create_all(bind=engine)
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db():
    try:
        db = SessionLocal()  # sessionを生成
        yield db
    finally:
        db.close()
    db.close()


@app.post("/token")
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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
def get_all_users(db: Session = Depends(get_db)):
    db_users = get_all_user_query(db=db)
    return db_users


@app.get("/users/{id}")
def get_user_by_id(id, db: Session = Depends(get_db)):
    db_user = get_user_by_id_query(db=db, id=id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User Not Found")
    return db_user


@app.get("/users/")
def get_user_by_name(name, db: Session = Depends(get_db)):
    db_user = get_user_by_username_query(db=db, username=name)
    if not db_user:
        raise HTTPException(status_code=400, detail="User Not Found")
    return db_user


@app.post("/exams", response_model=exam_schema.ExamScore)
def create_exam(
    exam: exam_schema.ExamScoreCreate,
    token: int = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    db_exam = get_examscore_by_title_query(
        db=db, userid=token, examtitle=exam.examtitle
    )
    if db_exam:
        raise HTTPException(status_code=400, detail="Same examtitle found")
    return create_exam_query(db=db, exam=exam, user_id=token)

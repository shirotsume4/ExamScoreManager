import models.schema.examscore_schema as exam_schema
from fastapi import Depends, HTTPException, APIRouter
from hashlib import sha256 as hash_func
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.dbengine.dbengine import Base, SessionLocal, engine
from models.dbengine.get_db import get_db
from usecases.examscore_usecase import (
    create_exam_query,
    get_examscore_by_title_query
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()
@router.post("/exams", tags=["exams"], response_model=exam_schema.ExamScore)
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

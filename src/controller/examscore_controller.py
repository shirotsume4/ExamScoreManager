from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import models.schema.examscore_schema as exam_schema
from db.get_db import get_db
from usecases.examscore_usecase import (
    create_exam_query,
    get_examscore_by_title_query,
    get_examscore_by_id_query,
    get_all_examscore_by_user_query,
    get_all_examscore_by_exam_query
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

@router.get('/exams/')
def get_all_exam(
    token: int = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    db_exam = get_all_examscore_by_user_query(db=db, userid=token)
    return db_exam

@router.get('/exams/{id}')
def get_exam_by_id(
    id: int,
    token: int = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    db_exam = get_examscore_by_id_query(db=db, id=id)
    if not db_exam:
        raise HTTPException(status_code=400, detail="Exam Not Found")
    return db_exam

@router.get('/exam/')
def get_exam_by_title(
    title: str,
    token: int = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    db_exam = get_examscore_by_title_query(db, userid=token,examtitle=title)
    if not db_exam:
        raise HTTPException(status_code=400, detail="Exam Not Found")
    return db_exam

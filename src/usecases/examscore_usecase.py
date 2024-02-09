from sqlalchemy.orm import Session

import models.schema.examscore_schema as schemas
from models.entity.examscore_entity import ExamScore


def get_examscore_by_title_query(db: Session, userid: int, examtitle: str):
    """get exam by title"""
    return (
        db.query(ExamScore)
        .filter(ExamScore.examtitle == examtitle and ExamScore.user_id == userid)
        .first()
    )


def get_examscore_by_id_query(db: Session, id: int):
    """get user by id"""
    return db.query(ExamScore).filter(ExamScore.id == id).first()


def get_all_examscore_by_user_query(db: Session, userid: int):
    """get all examscore by user"""
    return db.query(ExamScore).filter(ExamScore.user_id == userid).all()


def get_all_examscore_by_exam_query(db: Session, id: int):
    """get all examscore by examid"""
    return db.query(ExamScore).filter(ExamScore.id == id).all()


def create_exam_query(db: Session, exam: schemas.ExamScoreCreate, user_id: int):
    """create examscore"""
    db_exam = ExamScore(
        examtitle=exam.examtitle,
        user_id=user_id,
        english_score=exam.english_score,
        math_score=exam.math_score,
    )
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam

# app/routers/questions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..core.auth import get_current_subject

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.post("/", response_model=schemas.QuestionOut)
def create_question(
    q_in: schemas.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: models.Subject = Depends(get_current_subject)
):
    # Possibly only admin can create questions
    new_q = models.Question(
        question_text=q_in.question_text,
        question_type=q_in.question_type,
        min_scale=q_in.min_scale,
        max_scale=q_in.max_scale,
        step=q_in.step
    )
    db.add(new_q)
    db.commit()
    db.refresh(new_q)
    return new_q

@router.get("/", response_model=List[schemas.QuestionOut])
def list_questions(
    db: Session = Depends(get_db),
    current_user: models.Subject = Depends(get_current_subject)
):
    questions = db.query(models.Question).all()
    return questions

# app/routers/questions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.post("/", response_model=schemas.QuestionOut)
def create_question(question_in: schemas.QuestionCreate, db: Session = Depends(get_db)):
    new_question = models.Question(**question_in.dict())
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

@router.get("/", response_model=List[schemas.QuestionOut])
def list_questions(db: Session = Depends(get_db)):
    return db.query(models.Question).all()

@router.get("/{question_id}", response_model=schemas.QuestionOut)
def get_question(question_id: int, db: Session = Depends(get_db)):
    q = db.query(models.Question).get(question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found.")
    return q

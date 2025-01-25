# app/routers/subjects.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.post("/", response_model=schemas.SubjectOut)
def create_subject(subject_in: schemas.SubjectCreate, db: Session = Depends(get_db)):
    new_subject = models.Subject(**subject_in.dict())
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject

@router.get("/{subject_id}", response_model=schemas.SubjectOut)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(models.Subject).get(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found.")
    return subject

@router.get("/", response_model=List[schemas.SubjectOut])
def list_subjects(db: Session = Depends(get_db)):
    return db.query(models.Subject).all()

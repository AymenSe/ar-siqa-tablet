# app/routers/subjects.py

from random import random
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

# app/routers/subjects.py (new endpoints)
@router.post("/{subject_id}/assign-session", response_model=schemas.SessionOut)
def assign_session(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(models.Subject).get(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    # Check for existing incomplete session
    current_session = db.query(models.SubjectSession).filter_by(
        subject_id=subject_id,
        is_completed=False
    ).first()
    
    if current_session:
        return db.query(models.Session).get(current_session.session_id)
    
    # Assign training session first if not completed
    if not subject.has_completed_training:
        training_session = db.query(models.Session).filter_by(
            session_type=models.SessionType.TRAINING,
            is_active=True
        ).first()
        
        if not training_session:
            raise HTTPException(status_code=404, detail="No training session available")
        
        assignment = models.SubjectSession(
            subject_id=subject_id,
            session_id=training_session.session_id
        )
        db.add(assignment)
        db.commit()
        return training_session
    
    # Assign random real session
    completed_ids = [ss.session_id for ss in subject.sessions]
    available_sessions = db.query(models.Session).filter(
        models.Session.session_type == models.SessionType.REAL,
        models.Session.is_active == True,
        ~models.Session.session_id.in_(completed_ids)
    ).all()
    
    if not available_sessions:
        raise HTTPException(status_code=404, detail="No available sessions")
    
    selected_session = random.choice(available_sessions)
    assignment = models.SubjectSession(
        subject_id=subject_id,
        session_id=selected_session.session_id
    )
    db.add(assignment)
    db.commit()
    return selected_session

@router.post("/{subject_id}/complete-session")
def complete_session(subject_id: int, db: Session = Depends(get_db)):
    current_session = db.query(models.SubjectSession).filter_by(
        subject_id=subject_id,
        is_completed=False
    ).first()
    
    if not current_session:
        raise HTTPException(status_code=404, detail="No active session found")
    
    current_session.is_completed = True
    session = db.query(models.Session).get(current_session.session_id)
    
    if session.session_type == models.SessionType.TRAINING:
        subject = db.query(models.Subject).get(subject_id)
        subject.has_completed_training = True
    
    db.commit()
    return {"message": "Session marked as completed"}   
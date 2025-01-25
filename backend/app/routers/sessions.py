# app/routers/sessions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/", response_model=schemas.SessionOut)
def create_session(session_in: schemas.SessionCreate, db: Session = Depends(get_db)):
    # Ensure subject exists
    subject = db.query(models.Subject).get(session_in.subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found.")

    new_session = models.Session(
        subject_id=session_in.subject_id,
        session_type=session_in.session_type
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.get("/{session_id}", response_model=schemas.SessionOut)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session_obj = db.query(models.Session).get(session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found.")
    return session_obj

@router.get("/", response_model=List[schemas.SessionOut])
def list_sessions(db: Session = Depends(get_db)):
    return db.query(models.Session).all()

@router.patch("/{session_id}/complete", response_model=schemas.SessionOut)
def complete_session(session_id: int, db: Session = Depends(get_db)):
    session_obj = db.query(models.Session).get(session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found.")
    session_obj.is_completed = True
    db.commit()
    db.refresh(session_obj)
    return session_obj

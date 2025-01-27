from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/", response_model=schemas.SessionOut)
def create_session(session: schemas.SessionCreate, db: Session = Depends(get_db)):
    # Validate subject exists
    db_subject = db.query(models.Subject).get(session.subject_id)
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    new_session = models.Session(**session.dict())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.get("/{session_id}", response_model=schemas.SessionOut)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(models.Session).get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/", response_model=List[schemas.SessionOut])
def list_sessions(db: Session = Depends(get_db)):
    return db.query(models.Session).all()
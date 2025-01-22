# app/routers/subjects.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..core.security import get_password_hash
from ..core.auth import get_current_subject

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.post("/", response_model=schemas.SubjectOut)
def create_subject(subject_in: schemas.SubjectCreate, db: Session = Depends(get_db)):
    # Check username
    existing = db.query(models.Subject).filter(models.Subject.username == subject_in.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists.")
    hashed_pw = get_password_hash(subject_in.password)
    new_subject = models.Subject(
        username=subject_in.username,
        password_hash=hashed_pw,
        full_name=subject_in.full_name,
        age=subject_in.age,
        gender=subject_in.gender
    )
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject

@router.get("/me", response_model=schemas.SubjectOut)
def read_subject_me(current_user: models.Subject = Depends(get_current_subject)):
    return current_user

@router.get("/{subject_id}", response_model=schemas.SubjectOut)
def get_subject(subject_id: int, db: Session = Depends(get_db), current_user: models.Subject = Depends(get_current_subject)):
    # Possibly restrict so only admin or the same user can see
    subject = db.query(models.Subject).get(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found.")
    return subject

# app/routers/ratings.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.post("/", response_model=schemas.RatingOut)
def create_rating(rating: schemas.RatingCreate, db: Session = Depends(get_db)):
    # Validate session image exists
    session_image = db.query(models.SessionImage)\
        .options(joinedload(models.SessionImage.session))\
        .get(rating.session_image_id)
    
    if not session_image:
        raise HTTPException(status_code=404, detail="Session image not found")
    
    # Validate all question IDs exist
    question_ids = list(rating.question_ratings.keys())
    existing_questions = db.query(models.Question.question_id)\
        .filter(models.Question.question_id.in_(question_ids))\
        .all()
    existing_ids = {q[0] for q in existing_questions}
    if len(existing_ids) != len(question_ids):
        invalid_ids = set(question_ids) - existing_ids
        raise HTTPException(status_code=400, detail=f"Invalid question IDs: {invalid_ids}")
    
    # Create rating with denormalized data
    rating_data = rating.dict()
    rating_data.update({
        "subject_id": session_image.session.subject_id,
        "session_id": session_image.session_id,
        "image_id": session_image.image_id
    })
    
    new_rating = models.Rating(**rating_data)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

@router.get("/{rating_id}", response_model=schemas.RatingOut)
def get_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(models.Rating).get(rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

@router.get("/", response_model=List[schemas.RatingOut])
def list_ratings(db: Session = Depends(get_db)):
    return db.query(models.Rating).all()
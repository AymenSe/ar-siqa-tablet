# app/routers/ratings.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.post("/", response_model=schemas.RatingOut)
def create_rating(rating_in: schemas.RatingCreate, db: Session = Depends(get_db)):
    # Validate session_image
    si = db.query(models.SessionImage).get(rating_in.session_image_id)
    if not si:
        raise HTTPException(status_code=404, detail="SessionImage not found.")

    # Validate question
    question = db.query(models.Question).get(rating_in.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")

    new_rating = models.Rating(**rating_in.dict())
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

@router.get("/", response_model=List[schemas.RatingOut])
def list_ratings(db: Session = Depends(get_db)):
    return db.query(models.Rating).all()

@router.get("/{rating_id}", response_model=schemas.RatingOut)
def get_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(models.Rating).get(rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found.")
    return rating

# app/routers/ratings.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..core.auth import get_current_subject

router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.post("/", response_model=schemas.RatingOut)
def create_rating(
    rating_in: schemas.RatingCreate, 
    db: Session = Depends(get_db),
    current_user: models.Subject = Depends(get_current_subject)
):
    session_image = db.query(models.SessionImage).get(rating_in.session_image_id)
    if not session_image:
        raise HTTPException(status_code=404, detail="SessionImage not found.")

    # Ensure user is rating an image in their own session
    session_obj = db.query(models.Session).get(session_image.session_id)
    if session_obj.subject_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to rate this session's image.")

    question = db.query(models.Question).get(rating_in.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")

    existing_rating = db.query(models.Rating).filter(
        models.Rating.session_image_id == rating_in.session_image_id,
        models.Rating.question_id == rating_in.question_id
    ).first()
    if existing_rating:
        raise HTTPException(status_code=400, detail="Rating already submitted for this image/question.")

    new_rating = models.Rating(
        session_image_id=rating_in.session_image_id,
        question_id=rating_in.question_id,
        rating_value=rating_in.rating_value,
        text_answer=rating_in.text_answer,
        response_time=rating_in.response_time
    )
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    # Optionally update session's last_image_index
    # You can see what the display_order for session_image is:
    # if session_image.display_order > session_obj.last_image_index:
    #     session_obj.last_image_index = session_image.display_order
    #     db.commit()

    return new_rating

@router.get("/{rating_id}", response_model=schemas.RatingOut)
def get_rating(
    rating_id: int, 
    db: Session = Depends(get_db),
    current_user: models.Subject = Depends(get_current_subject)
):
    rating = db.query(models.Rating).get(rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found.")

    # Check ownership:
    session_image = db.query(models.SessionImage).get(rating.session_image_id)
    session_obj = db.query(models.Session).get(session_image.session_id)
    if session_obj.subject_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this rating.")

    return rating

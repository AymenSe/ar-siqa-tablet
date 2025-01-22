# app/routers/session_flow.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..core.auth import get_current_subject
from typing import Optional

router = APIRouter(prefix="/flow", tags=["Flow"])

@router.get("/next_image")
def get_next_image(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.Subject = Depends(get_current_subject)
):
    session_obj = db.query(models.Session).get(session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found.")
    if session_obj.subject_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this session.")

    if session_obj.is_completed:
        raise HTTPException(status_code=400, detail="Session is already completed.")

    # If you track progress in 'last_image_index'
    last_idx = session_obj.last_image_index or 0

    # Retrieve next session_image based on display_order
    next_session_image = (
        db.query(models.SessionImage)
        .filter(models.SessionImage.session_id == session_id,
                models.SessionImage.display_order > last_idx)
        .order_by(models.SessionImage.display_order.asc())
        .first()
    )
    if not next_session_image:
        # No more images => session completed
        session_obj.is_completed = True
        db.commit()
        raise HTTPException(status_code=200, detail="No more images. Session completed.")

    return {
        "session_image_id": next_session_image.id,
        "image_info": {
            "id": next_session_image.image.id,
            "file_name": next_session_image.image.file_name,
            "file_path": next_session_image.image.file_path
        },
        "display_order": next_session_image.display_order
    }

@router.post("/submit_rating")
def submit_rating_and_advance(
    rating_in: schemas.RatingCreate,
    db: Session = Depends(get_db),
    current_user: models.Subject = Depends(get_current_subject)
):
    # Reuse the logic from the ratings router or replicate here
    session_image = db.query(models.SessionImage).get(rating_in.session_image_id)
    if not session_image:
        raise HTTPException(status_code=404, detail="SessionImage not found.")

    session_obj = db.query(models.Session).get(session_image.session_id)
    if session_obj.subject_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized.")

    # Create rating
    question = db.query(models.Question).get(rating_in.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")

    existing = db.query(models.Rating).filter_by(
        session_image_id=rating_in.session_image_id,
        question_id=rating_in.question_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Rating already submitted.")

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

    # Update session's last_image_index if needed
    if session_image.display_order > (session_obj.last_image_index or 0):
        session_obj.last_image_index = session_image.display_order
        db.commit()

    # Return next image or indicate that the session is done
    return {"message": "Rating saved. You can call /flow/next_image to get the next image."}

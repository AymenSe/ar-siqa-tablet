# app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db


router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/sessions", response_model=schemas.SessionOut)
def create_session(session: schemas.SessionCreate, db: Session = Depends(get_db)):
    # Only one training session allowed
    if session.session_type == models.SessionType.TRAINING:
        existing = db.query(models.Session).filter_by(session_type=models.SessionType.TRAINING).first()
        if existing:
            raise HTTPException(status_code=400, detail="Training session already exists")
    
    new_session = models.Session(**session.dict())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.post("/sessions/{session_id}/images")
def add_images_to_session(
    session_id: int,
    image_ids: List[int],
    db: Session = Depends(get_db)
):
    session = db.query(models.Session).get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Validate images exist
    images = db.query(models.Image).filter(models.Image.image_id.in_(image_ids)).all()
    if len(images) != len(image_ids):
        missing = set(image_ids) - {img.image_id for img in images}
        raise HTTPException(status_code=404, detail=f"Missing images: {missing}")
    
    # Add images to session
    display_order = 1
    for img_id in image_ids:
        session_image = models.SessionImage(
            session_id=session_id,
            image_id=img_id,
            display_order=display_order,
            is_training=(session.session_type == models.SessionType.TRAINING)
        )
        db.add(session_image)
        display_order += 1
    
    db.commit()
    return {"message": f"Added {len(image_ids)} images to session"}
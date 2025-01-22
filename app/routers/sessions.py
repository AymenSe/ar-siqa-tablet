# app/routers/sessions.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..core.auth import get_current_subject

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/", response_model=schemas.SessionOut)
def create_session(
    session_in: schemas.SessionCreate, 
    db: Session = Depends(get_db),
    current_user: models.Subject = Depends(get_current_subject)
):
    # Check that the subject in the request is the same as the current_user OR admin
    if current_user.id != session_in.subject_id:
        # If you want only the user themselves to create their sessions
        raise HTTPException(status_code=403, detail="Not authorized to create session for this subject.")

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
def get_session(
    session_id: int, 
    db: Session = Depends(get_db),
    current_user: models.Subject = Depends(get_current_subject)
):
    session_obj = db.query(models.Session).get(session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found.")
    # Optionally restrict so that only the owner or admin can see it
    if session_obj.subject_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this session.")
    return session_obj

@router.patch("/{session_id}/complete", response_model=schemas.SessionOut)
def complete_session(
    session_id: int, 
    db: Session = Depends(get_db),
    current_user: models.Subject = Depends(get_current_subject)
):
    session_obj = db.query(models.Session).get(session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found.")
    if session_obj.subject_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to complete this session.")

    session_obj.is_completed = True
    db.commit()
    db.refresh(session_obj)
    return session_obj


@router.post("/{session_id}/assign_images", response_model=List[schemas.SessionImageOut])
def assign_images_to_session(
    session_id: int, 
    image_ids: List[int],  # or none if we randomize from all images
    db: Session = Depends(get_db),
    current_user: models.Subject = Depends(get_current_subject)
):
    session_obj = db.query(models.Session).get(session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found.")

    if session_obj.subject_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized.")

    # If no image_ids provided, randomize from all images in DB
    if not image_ids:
        all_image_ids = [img.id for img in db.query(models.Image).all()]
        # pick some random subset if needed
        import random
        random.shuffle(all_image_ids)
        image_ids = all_image_ids[:10]  # example picks 10

    # Assign them in random order
    import random
    random.shuffle(image_ids)
    
    session_images = []
    for order, img_id in enumerate(image_ids, start=1):
        si = models.SessionImage(
            session_id=session_id,
            image_id=img_id,
            display_order=order,
            is_training=(session_obj.session_type == "training")  # or your own logic
        )
        db.add(si)
        session_images.append(si)
    db.commit()

    # Refresh in one go
    for si in session_images:
        db.refresh(si)

    return session_images

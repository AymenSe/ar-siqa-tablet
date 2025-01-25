# app/routers/session_images.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

# router = APIRouter(prefix="/session-images", tags=["SessionImages"])

router = APIRouter(prefix="/session-images", tags=["Sessions Images"])


@router.post("/", response_model=schemas.SessionImageOut)
def create_session_image(si_in: schemas.SessionImageCreate, db: Session = Depends(get_db)):
    # Validate session and image exist
    session_obj = db.query(models.Session).get(si_in.session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found.")

    image_obj = db.query(models.Image).get(si_in.image_id)
    if not image_obj:
        raise HTTPException(status_code=404, detail="Image not found.")

    new_si = models.SessionImage(**si_in.dict())
    db.add(new_si)
    db.commit()
    db.refresh(new_si)
    return new_si

@router.get("/{session_image_id}", response_model=schemas.SessionImageOut)
def get_session_image(session_image_id: int, db: Session = Depends(get_db)):
    si = db.query(models.SessionImage).get(session_image_id)
    if not si:
        raise HTTPException(status_code=404, detail="SessionImage not found.")
    return si

# app/routers/session_images.py
@router.get("/", response_model=List[schemas.SessionImageOut])
def get_session_images(session_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all images assigned to a session.
    """
    session_images = (
        db.query(models.SessionImage)
        .filter(models.SessionImage.session_id == session_id)
        .join(models.Image, models.SessionImage.image_id == models.Image.image_id)
        .all()
    )

    if not session_images:
        raise HTTPException(status_code=404, detail="No images found for the session")

    return session_images


@router.post("/{session_id}/assign_images", response_model=List[schemas.SessionImageOut])
def assign_images_to_session(session_id: int, image_ids: List[int], db: Session = Depends(get_db)):
    """
    Assign a list of images to a session. Dynamically populate the Image table if needed.
    """
    import os

    # Base path for your static image folder
    static_image_folder = "backend/images"

    # Fetch the session from the database
    session = db.query(models.Session).filter(models.Session.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session_images = []
    for order, image_id in enumerate(image_ids, start=1):
        # Construct the file name and path
        file_name = f"{image_id}.jpg"  # Assuming files are named as `1.jpg`, `2.jpg`, etc.
        file_path = os.path.join(static_image_folder, file_name)

        # Check if the file exists locally
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail=f"File {file_path} not found")

        # Check if the image exists in the database; if not, create it
        image = db.query(models.Image).filter(models.Image.image_id == image_id).first()
        if not image:
            # Dynamically create a new image entry
            image = models.Image(
                image_id=image_id,
                file_name=file_name,
                file_path=file_path,
                description=f"Image {image_id}",
                
            )
            db.add(image)

        # Create a new session image
        session_image = models.SessionImage(
            session_id=session_id,
            image_id=image.image_id,
            display_order=order,
            is_training=(session.session_type.lower() == "training"),
        )
        db.add(session_image)
        session_images.append(session_image)

    # Commit all changes
    db.commit()
    # return session_images
    # Serialize the response to ensure datetime fields are strings
    response = [
        schemas.SessionImageOut(
            session_image_id=si.session_image_id,
            session_id=si.session_id,
            image_id=si.image_id,
            display_order=si.display_order,
            is_training=si.is_training,
            image={
                "image_id": si.image.image_id,
                "file_name": si.image.file_name,
                "file_path": si.image.file_path,
                "description": si.image.description,
                "created_at": si.image.created_at.isoformat() if si.image.created_at else None,
            } if si.image else None,
        )
        for si in session_images
    ]
    return response


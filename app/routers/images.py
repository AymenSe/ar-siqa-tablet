# app/routers/images.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..core.auth import get_current_subject

router = APIRouter(prefix="/images", tags=["Images"])

@router.post("/", response_model=schemas.ImageOut)
def create_image(
    image_in: schemas.ImageCreate, 
    db: Session = Depends(get_db),
    current_user: models.Subject = Depends(get_current_subject)
):
    # Possibly only admin can create images
    # if not current_user.is_admin:  # example
    #     raise HTTPException(status_code=403, detail="Not authorized to create images.")

    new_image = models.Image(
        file_name=image_in.file_name,
        file_path=image_in.file_path,
        category_id=image_in.category_id,
        description=image_in.description
    )
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image

@router.get("/", response_model=List[schemas.ImageOut])
def list_images(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.Subject = Depends(get_current_subject)
):
    images = db.query(models.Image).offset(skip).limit(limit).all()
    return images

@router.get("/{image_id}", response_model=schemas.ImageOut)
def get_image(image_id: int, db: Session = Depends(get_db), current_user: models.Subject = Depends(get_current_subject)):
    image = db.query(models.Image).get(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found.")
    return image

# app/routers/images.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/images", tags=["Images"])

@router.post("/", response_model=schemas.ImageOut)
def create_image(image: schemas.ImageCreate, db: Session = Depends(get_db)):
    # Check for existing file name
    existing = db.query(models.Image).filter(models.Image.file_name == image.file_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="File name already exists")
    
    new_image = models.Image(**image.dict())
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image

@router.get("/{image_id}", response_model=schemas.ImageOut)
def get_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(models.Image).get(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image

@router.get("/", response_model=List[schemas.ImageOut])
def list_images(db: Session = Depends(get_db)):
    return db.query(models.Image).all()
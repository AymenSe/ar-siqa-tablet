# app/routers/flow.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db

router = APIRouter(prefix="/flow", tags=["Flow"])

@router.get("/next_image")
def get_next_image(session_id: int, db: Session = Depends(get_db)):
    # Check session
    session_obj = db.query(models.Session).get(session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found.")
    if session_obj.is_completed:
        return {"message": "Session is already completed."}

    # Retrieve last_image_index from your session logic if you store it in the session table
    # For now, let's assume we have session_obj.last_image_index
    last_idx = session_obj.last_image_index or 0

    next_si = (
        db.query(models.SessionImage)
        .filter(models.SessionImage.session_id == session_id,
                models.SessionImage.display_order > last_idx)
        .order_by(models.SessionImage.display_order.asc())
        .first()
    )
    if not next_si:
        # no more images
        session_obj.is_completed = True
        db.commit()
        return {"message": "No more images. Session completed."}

    return {
        "session_image_id": next_si.session_image_id,
        "image_info": {
            "id": next_si.image.image_id,
            "file_name": next_si.image.file_name,
            "file_path": next_si.image.file_path
        },
        "display_order": next_si.display_order
    }

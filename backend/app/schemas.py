# app/schemas.py
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

# Helper so we don't repeat from_attributes each time
class ConfigMixin:
    model_config = {
        "from_attributes": True
    }

# ---------------------
# SUBJECT
# ---------------------
class SubjectBase(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectOut(SubjectBase, ConfigMixin):
    subject_id: int
    created_at: Optional[datetime] = None

# ---------------------
# SESSION
# ---------------------
class SessionBase(BaseModel):
    session_type: str

class SessionCreate(SessionBase):
    subject_id: int

class SessionOut(SessionBase, ConfigMixin):
    session_id: int
    subject_id: int
    is_completed: bool
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    

# ---------------------
# IMAGE
# ---------------------
class ImageBase(BaseModel):
    file_name: str
    file_path: Optional[str] = None
    description: Optional[str] = None

class ImageCreate(ImageBase):
    pass

class ImageOut(ImageBase, ConfigMixin):
    image_id: int
    created_at: Optional[datetime] = None  # Expecting string for `created_at`



# ---------------------
# SESSION IMAGE
# ---------------------
class SessionImageBase(BaseModel):
    session_id: int
    image_id: int
    display_order: int
    is_training: bool = False
    # session_type: str

class SessionImageCreate(SessionImageBase):
    pass

class SessionImageOut(SessionImageBase, ConfigMixin):
    session_image_id: int
    session_id: int
    image_id: int
    display_order: int
    is_training: bool
    image: Optional[ImageOut] = None  # <--- Add a nested image

    model_config = {
        "from_attributes": True
    }


# ---------------------
# QUESTION
# ---------------------
class QuestionBase(BaseModel):
    question_text: str
    question_type: str = "likert"
    min_scale: Optional[int] = None
    max_scale: Optional[int] = None
    step: Optional[int] = 1

class QuestionCreate(QuestionBase):
    pass

class QuestionOut(QuestionBase, ConfigMixin):
    question_id: int

# ---------------------
# RATING
# ---------------------
class RatingBase(BaseModel):
    rating_value: Optional[float] = None
    text_answer: Optional[str] = None
    response_time: Optional[float] = None

class RatingCreate(RatingBase):
    session_image_id: int
    question_id: int

class RatingOut(RatingBase, ConfigMixin):
    rating_id: int
    session_image_id: int
    question_id: int
    created_at: Optional[datetime] = None

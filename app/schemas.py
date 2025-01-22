# app/schemas.py
from pydantic import BaseModel
from typing import Optional, List

# ----------------------------------------------------------------
# AUTH / TOKEN
# ----------------------------------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

# ----------------------------------------------------------------
# SUBJECTS
# ----------------------------------------------------------------
class SubjectBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

class SubjectCreate(SubjectBase):
    password: str

class SubjectOut(SubjectBase):
    id: int

    class Config:
        orm_mode = True

# ----------------------------------------------------------------
# IMAGES
# ----------------------------------------------------------------
class ImageBase(BaseModel):
    file_name: str
    file_path: Optional[str] = None
    description: Optional[str] = None

class ImageCreate(ImageBase):
    category_id: Optional[int] = None

class ImageOut(ImageBase):
    id: int
    category_id: Optional[int] = None
    
    class Config:
        orm_mode = True

# ----------------------------------------------------------------
# QUESTIONS
# ----------------------------------------------------------------
class QuestionBase(BaseModel):
    question_text: str
    question_type: str = "likert"
    min_scale: Optional[int] = None
    max_scale: Optional[int] = None
    step: Optional[int] = 1

class QuestionCreate(QuestionBase):
    pass

class QuestionOut(QuestionBase):
    id: int

    class Config:
        orm_mode = True

# ----------------------------------------------------------------
# SESSIONS
# ----------------------------------------------------------------
class SessionBase(BaseModel):
    session_type: str

class SessionCreate(SessionBase):
    subject_id: int

class SessionOut(SessionBase):
    id: int
    subject_id: int
    is_completed: bool

    class Config:
        orm_mode = True

# ----------------------------------------------------------------
# RATINGS
# ----------------------------------------------------------------
class RatingBase(BaseModel):
    rating_value: Optional[float] = None
    text_answer: Optional[str] = None
    response_time: Optional[float] = None

class RatingCreate(RatingBase):
    session_image_id: int
    question_id: int

class RatingOut(RatingBase):
    id: int
    session_image_id: int
    question_id: int

    class Config:
        orm_mode = True

# ----------------------------------------------------------------
# SESSION IMAGES
# ----------------------------------------------------------------
class SessionImageOut(BaseModel):
    id: int
    session_id: int
    image_id: int
    display_order: int
    is_training: bool

    class Config:
        orm_mode = True

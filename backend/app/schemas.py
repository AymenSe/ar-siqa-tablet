from datetime import datetime
from typing import Dict, Optional, Annotated
from pydantic import BaseModel, Field
from sqlalchemy import Enum

class ConfigMixin(BaseModel):
    model_config = {"from_attributes": True}

# ---------------------
# SUBJECT
# ---------------------
class SubjectBase(BaseModel):
    name: str
    age: Optional[Annotated[int, Field(ge=1, le=120)]] = None
    gender: Optional[str] = Field(None, max_length=25)

class SubjectCreate(SubjectBase):
    pass

class SubjectOut(SubjectBase, ConfigMixin):
    subject_id: int
    created_at: datetime

# ---------------------
# SESSION
# ---------------------
class SessionType(str, Enum):
    TRAINING = "training"
    REAL = "real"
    
class SessionBase(BaseModel):
    session_type: str = Field(..., example="training")

class SessionCreate(BaseModel):
    name: str = Field(..., max_length=100)
    session_type: SessionType
    description: Optional[str] = None

class SessionOut(SessionBase, ConfigMixin):
    session_id: int
    subject_id: int
    is_completed: bool
    is_active: bool
    start_time: datetime
    end_time: Optional[datetime] = None

# ---------------------
# IMAGE
# ---------------------
class ImageBase(BaseModel):
    file_name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=200)

class ImageCreate(ImageBase):
    pass

class ImageOut(ImageBase, ConfigMixin):
    image_id: int
    created_at: datetime

# ---------------------
# SESSION IMAGE
# ---------------------
class SessionImageBase(BaseModel):
    display_order: Annotated[int, Field(ge=1)]
    is_training: bool

class SessionImageCreate(SessionImageBase):
    session_id: int
    image_id: int

class SessionImageOut(SessionImageBase, ConfigMixin):
    session_image_id: int
    session_id: int
    image_id: int
    image: ImageOut  # Nested image data

# ---------------------
# QUESTION
# ---------------------
class QuestionBase(BaseModel):
    text: str = Field(..., max_length=200)
    category: str = Field(..., max_length=50)

class QuestionCreate(QuestionBase):
    pass

class QuestionOut(QuestionBase, ConfigMixin):
    question_id: int

# ---------------------
# RATING
# ---------------------
class RatingBase(BaseModel):
    question_ratings: Dict[int, Annotated[int, Field(ge=1, le=5)]] = Field(
        ...,
        example={1: 4, 2: 5},
        description="QuestionID -> Rating (1-5)"
    )

class RatingCreate(RatingBase):
    session_image_id: int

class RatingOut(RatingCreate, ConfigMixin):
    rating_id: int
    created_at: datetime
    subject_id: int  # Denormalized for easier analytics
    session_id: int  # Denormalized from session_image
    image_id: int    # Denormalized from session_image
# app/models.py
from sqlalchemy import Column, Enum, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Subject(Base):
    __tablename__ = "subjects"
    
    subject_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(25), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sessions = relationship("Session", back_populates="subject")


class SessionType(str, Enum):
    TRAINING = "training"
    REAL = "real"
    
class Session(Base):
    __tablename__ = "sessions"
    
    session_id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"))
    session_type = Column(Enum(SessionType), nullable=False)  # Changed to enum
    is_active = Column(Boolean, default=True)  # New field to enable/disable sessions
    is_completed = Column(Boolean, default=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    
    subject = relationship("Subject", back_populates="sessions")
    session_images = relationship("SessionImage", back_populates="session")

class Image(Base):
    __tablename__ = "images"
    
    image_id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(100), unique=True, nullable=False)
    description = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session_images = relationship("SessionImage", back_populates="image")

class SessionImage(Base):
    __tablename__ = "session_images"
    
    session_image_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.session_id"))
    image_id = Column(Integer, ForeignKey("images.image_id"))
    display_order = Column(Integer, nullable=False)
    is_training = Column(Boolean, default=False)
    
    session = relationship("Session", back_populates="session_images")
    image = relationship("Image", back_populates="session_images")
    ratings = relationship("Rating", back_populates="session_image")

    
class Question(Base):
    __tablename__ = "questions"
    
    question_id = Column(Integer, primary_key=True, index=True)
    text = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)


class SubjectSession(Base):
    __tablename__ = "subject_sessions"
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"))
    session_id = Column(Integer, ForeignKey("sessions.session_id"))
    is_completed = Column(Boolean, default=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    
class Rating(Base):
    __tablename__ = "ratings"
    
    rating_id = Column(Integer, primary_key=True, index=True)
    session_image_id = Column(Integer, ForeignKey("session_images.session_image_id"))
    question_ratings = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Denormalized fields for faster queries
    subject_id = Column(Integer, nullable=False)
    session_id = Column(Integer, nullable=False)
    image_id = Column(Integer, nullable=False)
    
    session_image = relationship("SessionImage", back_populates="ratings")
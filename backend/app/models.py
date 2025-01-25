# app/models.py

from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, Float, Text, TIMESTAMP
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Subject(Base):
    __tablename__ = "subjects"

    subject_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(20), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    # Relationship: one subject -> many sessions
    sessions = relationship("Session", back_populates="subject")

class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"), nullable=False)
    session_type = Column(String(50), nullable=False)  # e.g., "training", "block1"
    start_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    end_time = Column(TIMESTAMP, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)

    # Relationship to Subject
    subject = relationship("Subject", back_populates="sessions")

    # Relationship: one session -> many session_images
    session_images = relationship("SessionImage", back_populates="session")

class Image(Base):
    __tablename__ = "images"

    image_id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

class SessionImage(Base):
    __tablename__ = "session_images"

    session_image_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.session_id"), nullable=False)
    image_id = Column(Integer, ForeignKey("images.image_id"), nullable=False)
    display_order = Column(Integer, nullable=False)
    is_training = Column(Boolean, default=False, nullable=False)

    # Relationship to Session
    session = relationship("Session", back_populates="session_images")
    # Relationship to Image
    image = relationship("Image", backref="session_images")
    # Relationship to Ratings
    ratings = relationship("Rating", back_populates="session_image")

class Question(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), default="likert", nullable=False)
    min_scale = Column(Integer, nullable=True)
    max_scale = Column(Integer, nullable=True)
    step = Column(Integer, default=1, nullable=True)

class Rating(Base):
    __tablename__ = "ratings"

    rating_id = Column(Integer, primary_key=True, index=True)
    session_image_id = Column(Integer, ForeignKey("session_images.session_image_id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.question_id"), nullable=False)
    rating_value = Column(Float, nullable=True)
    text_answer = Column(Text, nullable=True)
    response_time = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    # Relationship to SessionImage
    session_image = relationship("SessionImage", back_populates="ratings")
    # Relationship to Question
    question = relationship("Question", backref="ratings")

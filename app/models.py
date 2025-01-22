from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255))
    full_name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    # relationships
    sessions = relationship("Session", back_populates="subject")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500))
    category_id = Column(Integer, ForeignKey("categories.id"))
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    # relationship
    category = relationship("Category", backref="images")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False, default='likert')
    min_scale = Column(Integer)
    max_scale = Column(Integer)
    step = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    session_type = Column(String(50), nullable=False)
    start_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    end_time = Column(TIMESTAMP)
    is_completed = Column(Boolean, default=False, nullable=False)
    last_image_index = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    subject = relationship("Subject", back_populates="sessions")
    session_images = relationship("SessionImage", back_populates="session")


class SessionImage(Base):
    __tablename__ = "session_images"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    display_order = Column(Integer, nullable=False)
    is_training = Column(Boolean, default=False, nullable=False)

    session = relationship("Session", back_populates="session_images")
    image = relationship("Image", backref="session_images")


class SessionQuestion(Base):
    __tablename__ = "session_questions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    display_order = Column(Integer, nullable=False)


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    session_image_id = Column(Integer, ForeignKey("session_images.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    rating_value = Column(Float)
    text_answer = Column(Text)
    response_time = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    # relationships
    session_image = relationship("SessionImage", backref="ratings")
    question = relationship("Question", backref="ratings")

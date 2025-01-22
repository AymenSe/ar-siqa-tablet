# app/main.py
from fastapi import FastAPI
from .database import Base, engine
from .routers import auth, subjects, sessions, images, questions, ratings, session_flow

# For development only (create tables if they don't exist)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quality Assessment Experiment API")

# Register Routers
app.include_router(auth.router)
app.include_router(subjects.router)
app.include_router(sessions.router)
app.include_router(images.router)
app.include_router(questions.router)
app.include_router(ratings.router)
app.include_router(session_flow.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Quality Assessment Experiment API"}

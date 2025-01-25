# app/main.py

from fastapi import FastAPI
from .database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from .routers import (
    subjects, sessions, images, session_images, questions, ratings, flow
)
from fastapi.staticfiles import StaticFiles



# Create the tables at startup (development only)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Subjective Quality Experiment (Revised Schema)")

# Mount the 'images' folder as a static route
app.mount("/backend/images", StaticFiles(directory="backend/images"), name="images")

# Allow requests from localhost:3000
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(subjects.router)
app.include_router(sessions.router)
app.include_router(images.router)
app.include_router(session_images.router)
app.include_router(questions.router)
app.include_router(ratings.router)
app.include_router(flow.router)  # optional

@app.get("/")
def root():
    return {"message": "Revised Schema Experiment API running"}

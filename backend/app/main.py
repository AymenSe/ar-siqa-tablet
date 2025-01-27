from fastapi import FastAPI
from .database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from .routers import (
    subjects, sessions, images, session_images, questions, ratings, flow, admin
)
from fastapi.staticfiles import StaticFiles
import signal
import sys

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
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Revised Schema Experiment API running"}

# Graceful shutdown handler
def handle_shutdown(signal, frame):
    print("\nShutting down server gracefully...")
    sys.exit(0)

# Register the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, handle_shutdown)

if __name__ == "__main__":
    import uvicorn
    try:
        # Start the server
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except KeyboardInterrupt:
        # Handle Ctrl+C explicitly
        print("\nServer interrupted by user (Ctrl+C). Shutting down...")
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
    finally:
        # Perform any cleanup here
        print("Server shutdown complete.")
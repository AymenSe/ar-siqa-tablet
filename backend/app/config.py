# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SQLITE_URL: str = "sqlite:///./mydatabase.db"
    SECRET_KEY: str = "ANY_SECRET_KEY"  # only if needed for other features

    class Config:
        env_file = ".env"  # optional
        

settings = Settings()

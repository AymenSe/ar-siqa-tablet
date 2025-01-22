import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "experiment_db"

    # For a production environment, you might use environment variables:
    # POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
    # ...

    # Other config: secret keys, debugging, etc.
    SECRET_KEY: str = "YOUR_SECRET_KEY"

    class Config:
        env_file = ".env"  # if you want to load from a .env file

settings = Settings()

from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql://user:password@localhost/dbname"

    # JWT settings
    jwt_secret_key: str = "your-super-secret-jwt-signing-key-here"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30

    # Environment
    environment: str = "development"

    # API settings
    api_prefix: str = "/api"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields that might be in .env


# Initialize settings
settings = Settings()

# Validate that database_url is not the default placeholder
if settings.database_url == "postgresql://user:password@localhost/dbname":
    # Try to get from environment directly as fallback
    db_url_from_env = os.getenv("DATABASE_URL")
    if db_url_from_env:
        settings.database_url = db_url_from_env
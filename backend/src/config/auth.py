"""
Authentication configuration settings
"""
from pydantic import BaseSettings
from typing import Optional
import os


class AuthSettings(BaseSettings):
    # JWT settings
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-signing-key-here")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expiration_minutes: int = int(os.getenv("JWT_EXPIRATION_MINUTES", "30"))

    # Better Auth settings
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "")
    better_auth_url: str = os.getenv("BETTER_AUTH_URL", "")

    # Security settings
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    class Config:
        env_file = ".env"
        case_sensitive = True


# Initialize auth settings
auth_settings = AuthSettings()
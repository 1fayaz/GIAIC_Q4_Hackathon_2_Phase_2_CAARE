from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config.settings import settings
import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import Field


# Generate UUIDs for models
def generate_uuid():
    return str(uuid.uuid4())


# Base model with common fields
class BaseModel(SQLModel):
    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Note: Async engine is created in the main application file to avoid import-time conflicts
# Database engine and session setup happens in database.py for sync operations
# and in the main application for async operations
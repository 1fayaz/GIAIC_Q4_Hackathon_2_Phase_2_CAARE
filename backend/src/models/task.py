from sqlmodel import Field, SQLModel
from typing import Optional
from .base import BaseModel
import uuid
from datetime import datetime


class TaskBase(SQLModel):
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: str = Field(foreign_key="user.id")


class Task(TaskBase, table=True):
    """
    Task model representing a task item owned by a specific user
    """
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(TaskBase):
    """
    Schema for creating a new task
    """
    title: str
    user_id: str


class TaskRead(TaskBase):
    """
    Schema for reading task data
    """
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """
    Schema for updating a task
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
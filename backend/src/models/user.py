from sqlmodel import Field, SQLModel
from typing import Optional
from .base import BaseModel
import uuid
from datetime import datetime
from passlib.context import CryptContext


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)


class User(UserBase, table=True):
    """
    User model representing an authenticated user in the system
    """
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def verify_password(self, password: str) -> bool:
        """
        Verify a plaintext password against the stored hashed password
        """
        return pwd_context.verify(password, self.hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Hash a plaintext password
        """
        return pwd_context.hash(password)


class UserCreate(UserBase):
    """
    Schema for creating a new user
    """
    password: str


class UserUpdate(SQLModel):
    """
    Schema for updating user data
    """
    email: Optional[str] = None
    password: Optional[str] = None


class UserRead(UserBase):
    """
    Schema for reading user data
    """
    id: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserLogin(SQLModel):
    """
    Schema for user login
    """
    email: str
    password: str


class UserPublic(UserBase):
    """
    Public representation of user data (without sensitive information)
    """
    id: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
"""
Authentication schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """
    Schema for token response
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for token data
    """
    user_id: Optional[str] = None
    email: Optional[str] = None


class UserRegisterRequest(BaseModel):
    """
    Schema for user registration request
    """
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class UserRegisterResponse(BaseModel):
    """
    Schema for user registration response
    """
    id: str
    email: str
    is_active: bool
    is_verified: bool
    created_at: str

    class Config:
        schema_extra = {
            "example": {
                "id": "uuid-string",
                "email": "user@example.com",
                "is_active": True,
                "is_verified": False,
                "created_at": "2023-01-01T00:00:00.000000Z"
            }
        }


class UserLoginRequest(BaseModel):
    """
    Schema for user login request
    """
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class UserLoginResponse(BaseModel):
    """
    Schema for user login response
    """
    access_token: str
    token_type: str
    user_id: str
    email: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "jwt-token-string",
                "token_type": "bearer",
                "user_id": "uuid-string",
                "email": "user@example.com"
            }
        }


class UserProfileResponse(BaseModel):
    """
    Schema for user profile response
    """
    id: str
    email: str
    is_active: bool
    is_verified: bool
    created_at: str
    updated_at: str

    class Config:
        schema_extra = {
            "example": {
                "id": "uuid-string",
                "email": "user@example.com",
                "is_active": True,
                "is_verified": False,
                "created_at": "2023-01-01T00:00:00.000000Z",
                "updated_at": "2023-01-01T00:00:00.000000Z"
            }
        }


class PasswordChangeRequest(BaseModel):
    """
    Schema for password change request
    """
    current_password: str
    new_password: str

    class Config:
        schema_extra = {
            "example": {
                "current_password": "oldpassword123",
                "new_password": "newpassword456"
            }
        }


class PasswordChangeResponse(BaseModel):
    """
    Schema for password change response
    """
    success: bool
    message: str

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Password changed successfully"
            }
        }
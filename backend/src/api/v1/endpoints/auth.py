"""
Authentication endpoints for user registration, login, and logout
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.database import get_session
from src.api.deps import get_current_user_dep
from src.services.auth_service import AuthService
from src.models.user import UserCreate, UserLogin
from src.schemas.auth import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserLoginRequest,
    UserLoginResponse,
    Token
)
from src.utils.security import handle_bad_request, handle_not_found


router = APIRouter()


@router.post("/auth/register", response_model=UserRegisterResponse, tags=["auth"])
def register_user(
    user_register: UserRegisterRequest,
    session: Session = Depends(get_session)
):
    """
    Register a new user account
    """
    try:
        # Convert request to UserCreate model
        user_create = UserCreate(
            email=user_register.email,
            password=user_register.password
        )

        # Register the user
        db_user = AuthService.register_user(session, user_create)

        # Return user info
        return UserRegisterResponse(
            id=db_user.id,
            email=db_user.email,
            is_active=db_user.is_active,
            is_verified=db_user.is_verified,
            created_at=str(db_user.created_at)
        )
    except ValueError as e:
        raise handle_bad_request(str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@router.post("/auth/login", response_model=UserLoginResponse, tags=["auth"])
def login_user(
    user_login: UserLoginRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return access token
    """
    try:
        # Convert request to UserLogin model
        user_credentials = UserLogin(
            email=user_login.email,
            password=user_login.password
        )

        # Attempt to login the user
        result = AuthService.login_user(session, user_credentials)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Return login response with token
        return UserLoginResponse(**result)
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )


@router.post("/auth/token", response_model=Token, tags=["auth"])
def get_token(
    user_login: UserLoginRequest,
    session: Session = Depends(get_session)
):
    """
    Get access token for user (alternative to login endpoint)
    """
    try:
        # Convert request to UserLogin model
        user_credentials = UserLogin(
            email=user_login.email,
            password=user_login.password
        )

        # Attempt to login the user
        result = AuthService.login_user(session, user_credentials)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Return token only
        return Token(
            access_token=result["access_token"],
            token_type=result["token_type"]
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during token generation"
        )


@router.get("/auth/me", tags=["auth"])
def get_current_user_profile(
    current_user: dict = Depends(get_current_user_dep)
):
    """
    Get current user's profile information
    """
    return current_user


@router.post("/auth/logout", tags=["auth"])
def logout_user():
    """
    Logout the current user
    """
    # In a stateless JWT system, logout is typically handled on the client side
    # by removing the token. Server-side, we just return a success response.
    return {"message": "Successfully logged out"}
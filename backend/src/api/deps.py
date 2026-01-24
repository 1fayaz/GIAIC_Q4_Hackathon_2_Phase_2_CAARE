from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from src.database import get_session
from src.utils.security import get_current_user
from src.models.user import User


# Initialize HTTP Bearer security scheme
security = HTTPBearer()


def get_current_user_dep(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> dict:
    """
    Dependency to get the current authenticated user from the JWT token
    """
    # Get user info from security utility
    user_info = get_current_user(credentials)

    # Optionally verify user exists in the database
    user = session.get(User, user_info["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists"
        )

    return user_info


def get_current_active_user(current_user: dict = Depends(get_current_user_dep)) -> dict:
    """
    Dependency to get the current active user
    """
    # Additional checks can be added here (e.g., account status, permissions)
    return current_user


def require_same_user(
    current_user: dict = Depends(get_current_user_dep),
    user_id: str = None
) -> bool:
    """
    Dependency to ensure the current user matches the requested user_id
    """
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
    return True


def get_user_if_authorized(
    user_id: str,
    current_user: dict = Depends(get_current_user_dep)
) -> dict:
    """
    Dependency to get user info if authorized to access the user's resources
    """
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
    return current_user


def get_session_dep(session: Session = Depends(get_session)) -> Generator:
    """
    Dependency to get database session
    """
    yield session
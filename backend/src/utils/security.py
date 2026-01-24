from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict
from src.utils.jwt_utils import verify_token
from src.config.settings import settings
from passlib.context import CryptContext
from datetime import datetime


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize HTTP Bearer security scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password

    Args:
        plain_password: Plaintext password to verify
        hashed_password: Hashed password to compare against

    Returns:
        True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for a plaintext password

    Args:
        password: Plaintext password to hash

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """
    Get the current user from the JWT token in the Authorization header
    """
    token = credentials.credentials

    # Verify the token
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user information from the token
    user_id = payload.get("sub")
    email = payload.get("email")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"user_id": user_id, "email": email}


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from JWT token

    Args:
        token: JWT token string

    Returns:
        User ID if found and token is valid, None otherwise
    """
    payload = verify_token(token)
    if payload:
        user_id = payload.get("sub")
        if user_id:
            return str(user_id)
    return None


def get_email_from_token(token: str) -> Optional[str]:
    """
    Extract email from JWT token

    Args:
        token: JWT token string

    Returns:
        Email if found and token is valid, None otherwise
    """
    payload = verify_token(token)
    if payload:
        email = payload.get("email")
        if email:
            return str(email)
    return None


def is_token_valid(token: str) -> bool:
    """
    Check if a JWT token is valid (not expired and properly formatted)

    Args:
        token: JWT token string

    Returns:
        True if token is valid, False otherwise
    """
    return verify_token(token) is not None


def get_token_expiration(token: str) -> Optional[datetime]:
    """
    Get the expiration datetime from a JWT token

    Args:
        token: JWT token string

    Returns:
        Expiration datetime if found and token is valid, None otherwise
    """
    payload = verify_token(token)
    if payload:
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            return datetime.fromtimestamp(exp_timestamp)
    return None


def verify_user_owns_resource(user_id: str, resource_user_id: str) -> bool:
    """
    Verify that the authenticated user owns the resource they're trying to access
    """
    return user_id == resource_user_id


def handle_forbidden_access(detail: str = "Access forbidden") -> HTTPException:
    """
    Create a standardized forbidden access exception
    """
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail
    )


def handle_not_found(resource: str = "Resource") -> HTTPException:
    """
    Create a standardized not found exception
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} not found"
    )


def handle_bad_request(detail: str = "Invalid request") -> HTTPException:
    """
    Create a standardized bad request exception
    """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )
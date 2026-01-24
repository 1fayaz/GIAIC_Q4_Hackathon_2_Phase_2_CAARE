"""
Authentication service for handling user registration, login, and token management
"""
from sqlmodel import Session, select
from typing import Optional
from src.models.user import User, UserCreate, UserLogin
from src.utils.jwt_utils import create_access_token
from src.utils.security import verify_password


class AuthService:
    """
    Service class for handling authentication-related operations
    """

    @staticmethod
    def register_user(session: Session, user_create: UserCreate) -> User:
        """
        Register a new user with the provided details

        Args:
            session: Database session
            user_create: User creation details (email, password)

        Returns:
            Created User object
        """
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            raise ValueError("User with this email already exists")

        # Hash the password
        hashed_password = User.hash_password(user_create.password)

        # Create new user
        db_user = User(
            email=user_create.email,
            hashed_password=hashed_password
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    @staticmethod
    def authenticate_user(session: Session, user_login: UserLogin) -> Optional[dict]:
        """
        Authenticate a user with provided credentials

        Args:
            session: Database session
            user_login: User login details (email, password)

        Returns:
            User object if authentication is successful, None otherwise
        """
        # Find user by email
        user = session.exec(select(User).where(User.email == user_login.email)).first()

        # Verify user exists and password is correct
        if not user or not verify_password(user_login.password, user.hashed_password):
            return None

        return user

    @staticmethod
    def login_user(session: Session, user_login: UserLogin) -> Optional[dict]:
        """
        Login a user and return authentication tokens

        Args:
            session: Database session
            user_login: User login details (email, password)

        Returns:
            Dictionary containing access token and user info if successful, None otherwise
        """
        user = AuthService.authenticate_user(session, user_login)

        if not user:
            return None

        # Create access token
        access_token_data = {
            "sub": user.id,
            "email": user.email
        }
        access_token = create_access_token(data=access_token_data)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "email": user.email
        }

    @staticmethod
    def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
        """
        Get a user by their ID

        Args:
            session: Database session
            user_id: User ID to look up

        Returns:
            User object if found, None otherwise
        """
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        return user

    @staticmethod
    def update_user_password(session: Session, user_id: str, new_password: str) -> bool:
        """
        Update a user's password

        Args:
            session: Database session
            user_id: ID of the user to update
            new_password: New password to set

        Returns:
            True if update was successful, False otherwise
        """
        user = AuthService.get_user_by_id(session, user_id)
        if not user:
            return False

        user.hashed_password = User.hash_password(new_password)
        session.add(user)
        session.commit()

        return True
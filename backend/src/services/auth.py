from typing import Optional
from src.models.user import User
from src.utils.jwt_utils import verify_password, hash_password, create_access_token
from sqlmodel import Session, select
from datetime import timedelta


class AuthService:
    """
    Service class for handling authentication-related business logic
    """

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password
        """
        # Query for the user by email
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if not user or not verify_password(password, user.hashed_password):
            return None

        return user

    @staticmethod
    def create_access_token_for_user(user: User) -> str:
        """
        Create an access token for a user
        """
        # Create data to encode in the token
        data = {
            "sub": user.id,
            "email": user.email,
            "role": "user"  # This can be extended for role-based access
        }

        # Set token expiration
        expires_delta = timedelta(minutes=30)

        # Create and return the token
        return create_access_token(data=data, expires_delta=expires_delta)

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Get a user by their email
        """
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    @staticmethod
    def register_user(session: Session, email: str, password: str) -> User:
        """
        Register a new user with email and password
        """
        # Hash the password
        hashed_password = hash_password(password)

        # Create a new user instance
        user = User(email=email, hashed_password=hashed_password)

        # Add the user to the session and commit
        session.add(user)
        session.commit()
        session.refresh(user)

        return user
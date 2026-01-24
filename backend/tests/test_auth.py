"""
Unit tests for authentication functionality
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from src.main import app
from src.database import engine, create_db_and_tables
from src.models.user import User, UserCreate
from src.services.auth_service import AuthService
from src.config.settings import settings


@pytest.fixture(scope="module")
def client():
    """Create a test client for the API"""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def db_session():
    """Create a database session for testing"""
    create_db_and_tables()

    with Session(engine) as session:
        yield session


def test_user_registration(client: TestClient, db_session: Session):
    """Test user registration endpoint"""
    # Clear any existing users with this email
    existing_user = db_session.exec(select(User).where(User.email == "test@example.com")).first()
    if existing_user:
        db_session.delete(existing_user)
        db_session.commit()

    # Register a new user
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "securepassword123"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == "test@example.com"
    assert data["is_active"] is True


def test_user_login_success(client: TestClient, db_session: Session):
    """Test successful user login"""
    # First register a user
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "login_test@example.com",
            "password": "securepassword123"
        }
    )
    assert register_response.status_code == 200

    # Then try to login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login_test@example.com",
            "password": "securepassword123"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user_id" in data
    assert "email" in data


def test_user_login_failure_invalid_credentials(client: TestClient, db_session: Session):
    """Test login failure with invalid credentials"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_user_login_failure_wrong_password(client: TestClient, db_session: Session):
    """Test login failure with wrong password"""
    # Register a user first
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "wrong_pass_test@example.com",
            "password": "correctpassword"
        }
    )
    assert register_response.status_code == 200

    # Try to login with wrong password
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrong_pass_test@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_protected_endpoint_without_auth(client: TestClient):
    """Test that protected endpoints require authentication"""
    # Try to access a protected task endpoint without auth
    response = client.get("/api/v1/user123/tasks")

    # Should return 401 Unauthorized due to missing auth header
    assert response.status_code == 401


def test_user_already_exists(client: TestClient, db_session: Session):
    """Test that registering a user with existing email fails"""
    # Register the first user
    first_reg = client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate_test@example.com",
            "password": "securepassword123"
        }
    )
    assert first_reg.status_code == 200

    # Try to register another user with the same email
    second_reg = client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate_test@example.com",
            "password": "anotherpassword456"
        }
    )

    # Should return 400 Bad Request
    assert second_reg.status_code == 422  # Validation error or 400


def test_token_generation_endpoint(client: TestClient, db_session: Session):
    """Test the token generation endpoint"""
    # Register a user first
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "token_test@example.com",
            "password": "securepassword123"
        }
    )
    assert register_response.status_code == 200

    # Use the token endpoint
    response = client.post(
        "/api/v1/auth/token",
        json={
            "email": "token_test@example.com",
            "password": "securepassword123"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_logout_endpoint(client: TestClient):
    """Test the logout endpoint"""
    response = client.post("/api/v1/auth/logout")

    # In a JWT stateless system, logout is typically just returning success
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Successfully logged out"


def test_auth_service_register_user(db_session: Session):
    """Test the authentication service register_user method directly"""
    # Clean up any existing test user
    existing_user = db_session.exec(select(User).where(User.email == "service_test@example.com")).first()
    if existing_user:
        db_session.delete(existing_user)
        db_session.commit()

    user_create = UserCreate(
        email="service_test@example.com",
        password="securepassword123"
    )

    user = AuthService.register_user(db_session, user_create)

    assert user.email == "service_test@example.com"
    assert user.is_active is True
    assert user.verify_password("securepassword123") is True


def test_auth_service_authenticate_user(db_session: Session):
    """Test the authentication service authenticate_user method directly"""
    # First create a user
    user_create = UserCreate(
        email="auth_service_test@example.com",
        password="securepassword123"
    )

    user = AuthService.register_user(db_session, user_create)
    assert user is not None

    # Now authenticate with correct credentials
    from src.models.user import UserLogin
    user_login = UserLogin(
        email="auth_service_test@example.com",
        password="securepassword123"
    )

    authenticated_user = AuthService.authenticate_user(db_session, user_login)

    assert authenticated_user is not None
    assert authenticated_user.email == "auth_service_test@example.com"

    # Test with wrong password
    wrong_login = UserLogin(
        email="auth_service_test@example.com",
        password="wrongpassword"
    )

    wrong_auth = AuthService.authenticate_user(db_session, wrong_login)

    assert wrong_auth is None
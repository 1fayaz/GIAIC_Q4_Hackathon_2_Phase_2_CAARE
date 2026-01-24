"""
Integration tests for authentication functionality
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from src.main import app
from src.database import engine, create_db_and_tables
from src.models.user import User
from src.models.task import Task, TaskCreate
from src.utils.jwt_utils import create_access_token


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


def test_end_to_end_auth_flow(client: TestClient, db_session: Session):
    """Test the complete authentication flow: register -> login -> access protected resource"""
    # Step 1: Register a new user
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "integration_test@example.com",
            "password": "securepassword123"
        }
    )
    assert register_response.status_code == 200
    register_data = register_response.json()
    user_id = register_data["id"]
    assert register_data["email"] == "integration_test@example.com"

    # Step 2: Login with the registered user
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "integration_test@example.com",
            "password": "securepassword123"
        }
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    access_token = login_data["access_token"]
    assert access_token is not None
    assert login_data["user_id"] == user_id

    # Step 3: Use the token to access protected endpoints
    headers = {"Authorization": f"Bearer {access_token}"}

    # Try to create a task for the user
    task_response = client.post(
        f"/api/v1/{user_id}/tasks",
        json={
            "title": "Integration test task",
            "description": "Task created during integration test",
            "user_id": user_id
        },
        headers=headers
    )
    assert task_response.status_code == 201
    task_data = task_response.json()
    task_id = task_data["id"]
    assert task_data["title"] == "Integration test task"

    # Step 4: Try to access the created task
    get_task_response = client.get(
        f"/api/v1/{user_id}/tasks/{task_id}",
        headers=headers
    )
    assert get_task_response.status_code == 200
    retrieved_task = get_task_response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["title"] == "Integration test task"

    # Step 5: Try to access another user's tasks (should fail)
    # First create another user
    other_user_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "other_user@example.com",
            "password": "otherpassword456"
        }
    )
    assert other_user_response.status_code == 200
    other_user_data = other_user_response.json()
    other_user_id = other_user_data["id"]

    # Login as the other user
    other_login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "other_user@example.com",
            "password": "otherpassword456"
        }
    )
    assert other_login_response.status_code == 200
    other_token = other_login_response.json()["access_token"]

    # Try to access the first user's task with the other user's token
    other_headers = {"Authorization": f"Bearer {other_token}"}
    unauthorized_response = client.get(
        f"/api/v1/{user_id}/tasks/{task_id}",
        headers=other_headers
    )
    # Should return 403 Forbidden
    assert unauthorized_response.status_code == 403


def test_user_isolation_in_list_tasks(client: TestClient, db_session: Session):
    """Test that users can only see their own tasks"""
    # Create first user
    user1_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "user1_isolation@test.com",
            "password": "password123"
        }
    )
    assert user1_response.status_code == 200
    user1_data = user1_response.json()
    user1_id = user1_data["id"]

    # Create second user
    user2_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "user2_isolation@test.com",
            "password": "password456"
        }
    )
    assert user2_response.status_code == 200
    user2_data = user2_response.json()
    user2_id = user2_data["id"]

    # Login as first user
    login1_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "user1_isolation@test.com",
            "password": "password123"
        }
    )
    assert login1_response.status_code == 200
    user1_token = login1_response.json()["access_token"]

    # Login as second user
    login2_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "user2_isolation@test.com",
            "password": "password456"
        }
    )
    assert login2_response.status_code == 200
    user2_token = login2_response.json()["access_token"]

    # Create a task for user1
    headers1 = {"Authorization": f"Bearer {user1_token}"}
    task1_response = client.post(
        f"/api/v1/{user1_id}/tasks",
        json={
            "title": "User 1 task",
            "description": "Task for user 1",
            "user_id": user1_id
        },
        headers=headers1
    )
    assert task1_response.status_code == 201
    task1_data = task1_response.json()
    task1_id = task1_data["id"]

    # Create a task for user2
    headers2 = {"Authorization": f"Bearer {user2_token}"}
    task2_response = client.post(
        f"/api/v1/{user2_id}/tasks",
        json={
            "title": "User 2 task",
            "description": "Task for user 2",
            "user_id": user2_id
        },
        headers=headers2
    )
    assert task2_response.status_code == 201
    task2_data = task2_response.json()
    task2_id = task2_data["id"]

    # User1 should only see their own task
    user1_tasks_response = client.get(
        f"/api/v1/{user1_id}/tasks",
        headers=headers1
    )
    assert user1_tasks_response.status_code == 200
    user1_tasks = user1_tasks_response.json()
    assert len(user1_tasks) == 1
    assert user1_tasks[0]["id"] == task1_id

    # User2 should only see their own task
    user2_tasks_response = client.get(
        f"/api/v1/{user2_id}/tasks",
        headers=headers2
    )
    assert user2_tasks_response.status_code == 200
    user2_tasks = user2_tasks_response.json()
    assert len(user2_tasks) == 1
    assert user2_tasks[0]["id"] == task2_id

    # User1 should not see user2's task
    # Try to access user2's tasks with user1's token
    user1_try_user2_tasks = client.get(
        f"/api/v1/{user2_id}/tasks",
        headers=headers1
    )
    # Should return 403 Forbidden
    assert user1_try_user2_tasks.status_code == 403


def test_jwt_token_validation(client: TestClient, db_session: Session):
    """Test JWT token validation in different scenarios"""
    # Register and login a user
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "jwt_test@example.com",
            "password": "securepassword123"
        }
    )
    assert register_response.status_code == 200
    user_data = register_response.json()
    user_id = user_data["id"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "jwt_test@example.com",
            "password": "securepassword123"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Test with valid token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(
        f"/api/v1/{user_id}/tasks",
        headers=headers
    )
    assert response.status_code == 200  # Should work with valid token

    # Test with malformed token
    malformed_headers = {"Authorization": "Bearer invalid.token.format"}
    malformed_response = client.get(
        f"/api/v1/{user_id}/tasks",
        headers=malformed_headers
    )
    assert malformed_response.status_code == 401  # Should fail with malformed token

    # Test with missing authorization header
    missing_auth_response = client.get(f"/api/v1/{user_id}/tasks")
    assert missing_auth_response.status_code == 401  # Should fail without auth header

    # Test with invalid token format
    invalid_format_response = client.get(
        f"/api/v1/{user_id}/tasks",
        headers={"Authorization": "InvalidFormat token"}
    )
    assert invalid_format_response.status_code == 401  # Should fail with wrong format


def test_auth_middleware_functionality(client: TestClient, db_session: Session):
    """Test that authentication middleware works correctly for different routes"""
    # Test that public routes don't require authentication
    health_response = client.get("/health")
    assert health_response.status_code == 200

    docs_response = client.get("/docs")
    # This might return 200 (redirect) or 404 depending on configuration
    # But it shouldn't return 401 unauthorized

    # Register a user to test protected routes
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "middleware_test@example.com",
            "password": "securepassword123"
        }
    )
    assert register_response.status_code == 200
    user_data = register_response.json()
    user_id = user_data["id"]

    # Try to access protected route without auth (should fail)
    protected_response = client.get(f"/api/v1/{user_id}/tasks")
    assert protected_response.status_code == 401

    # Login to get a token
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "middleware_test@example.com",
            "password": "securepassword123"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Now access protected route with valid token (should succeed)
    headers = {"Authorization": f"Bearer {token}"}
    protected_success_response = client.get(
        f"/api/v1/{user_id}/tasks",
        headers=headers
    )
    assert protected_success_response.status_code == 200
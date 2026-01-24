import pytest
from fastapi.testclient import TestClient
from src.main import app
from sqlmodel import Session, SQLModel, create_engine
from src.models.task import Task
from src.models.user import User
from src.database import get_session
from unittest.mock import MagicMock


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///test.db", echo=True, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_get_tasks_empty(client: TestClient):
    """
    Contract test for GET /api/{user_id}/tasks
    """
    # Mock user authentication
    mock_user_id = "test-user-id"

    # Call the endpoint
    response = client.get(f"/api/{mock_user_id}/tasks")

    # Assertions
    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client: TestClient, session: Session):
    """
    Contract test for POST /api/{user_id}/tasks
    """
    # Mock user authentication
    mock_user_id = "test-user-id"

    # Prepare test data
    task_data = {
        "title": "Test task",
        "description": "Test description",
        "user_id": mock_user_id
    }

    # Call the endpoint
    response = client.post(f"/api/{mock_user_id}/tasks", json=task_data)

    # Assertions
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["description"] == "Test description"
    assert data["user_id"] == mock_user_id
    assert "id" in data
    assert "created_at" in data


def test_get_specific_task(client: TestClient, session: Session):
    """
    Contract test for GET /api/{user_id}/tasks/{id}
    """
    # Mock user authentication
    mock_user_id = "test-user-id"

    # Create a task first
    task_data = {
        "title": "Test task",
        "description": "Test description",
        "user_id": mock_user_id
    }
    create_response = client.post(f"/api/{mock_user_id}/tasks", json=task_data)
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Call the endpoint to get the specific task
    response = client.get(f"/api/{mock_user_id}/tasks/{task_id}")

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test task"
    assert data["id"] == task_id


def test_update_task(client: TestClient, session: Session):
    """
    Contract test for PUT /api/{user_id}/tasks/{id}
    """
    # Mock user authentication
    mock_user_id = "test-user-id"

    # Create a task first
    task_data = {
        "title": "Original task",
        "description": "Original description",
        "user_id": mock_user_id
    }
    create_response = client.post(f"/api/{mock_user_id}/tasks", json=task_data)
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Prepare update data
    update_data = {
        "title": "Updated task",
        "description": "Updated description"
    }

    # Call the endpoint to update the task
    response = client.put(f"/api/{mock_user_id}/tasks/{task_id}", json=update_data)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated task"
    assert data["description"] == "Updated description"


def test_delete_task(client: TestClient, session: Session):
    """
    Contract test for DELETE /api/{user_id}/tasks/{id}
    """
    # Mock user authentication
    mock_user_id = "test-user-id"

    # Create a task first
    task_data = {
        "title": "Test task to delete",
        "description": "Test description",
        "user_id": mock_user_id
    }
    create_response = client.post(f"/api/{mock_user_id}/tasks", json=task_data)
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Call the endpoint to delete the task
    response = client.delete(f"/api/{mock_user_id}/tasks/{task_id}")

    # Assertions
    assert response.status_code == 204

    # Verify the task was deleted by trying to get it
    get_response = client.get(f"/api/{mock_user_id}/tasks/{task_id}")
    assert get_response.status_code == 404


def test_toggle_task_completion(client: TestClient, session: Session):
    """
    Contract test for PATCH /api/{user_id}/tasks/{id}/complete
    """
    # Mock user authentication
    mock_user_id = "test-user-id"

    # Create a task first
    task_data = {
        "title": "Test task",
        "description": "Test description",
        "user_id": mock_user_id
    }
    create_response = client.post(f"/api/{mock_user_id}/tasks", json=task_data)
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Call the endpoint to toggle task completion
    response = client.patch(f"/api/{mock_user_id}/tasks/{task_id}/complete")

    # Assertions
    assert response.status_code == 200
    data = response.json()
    # The completion status should be toggled (from default False to True)
    assert data["completed"] is True
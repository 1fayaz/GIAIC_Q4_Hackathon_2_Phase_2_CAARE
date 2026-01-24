import pytest
from fastapi.testclient import TestClient
from src.main import app
from sqlmodel import Session, SQLModel, create_engine
from src.database import get_session
from src.models.task import Task


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///test_integration.db", echo=True, connect_args={"check_same_thread": False})
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


def test_user_isolation_enforced(client: TestClient, session: Session):
    """
    Integration test for user isolation in task management
    """
    # Create tasks for user 1
    user1_id = "user1-id"
    user1_task_data = {
        "title": "User 1 task",
        "description": "This belongs to user 1",
        "user_id": user1_id
    }
    response1 = client.post(f"/api/{user1_id}/tasks", json=user1_task_data)
    assert response1.status_code == 201
    user1_task_id = response1.json()["id"]

    # Create tasks for user 2
    user2_id = "user2-id"
    user2_task_data = {
        "title": "User 2 task",
        "description": "This belongs to user 2",
        "user_id": user2_id
    }
    response2 = client.post(f"/api/{user2_id}/tasks", json=user2_task_data)
    assert response2.status_code == 201
    user2_task_id = response2.json()["id"]

    # Verify user 1 can only see their own tasks
    user1_tasks_response = client.get(f"/api/{user1_id}/tasks")
    assert user1_tasks_response.status_code == 200
    user1_tasks = user1_tasks_response.json()
    assert len(user1_tasks) == 1
    assert user1_tasks[0]["id"] == user1_task_id
    assert user1_tasks[0]["title"] == "User 1 task"

    # Verify user 2 can only see their own tasks
    user2_tasks_response = client.get(f"/api/{user2_id}/tasks")
    assert user2_tasks_response.status_code == 200
    user2_tasks = user2_tasks_response.json()
    assert len(user2_tasks) == 1
    assert user2_tasks[0]["id"] == user2_task_id
    assert user2_tasks[0]["title"] == "User 2 task"

    # Attempt to access another user's task (should fail)
    access_other_task_response = client.get(f"/api/{user1_id}/tasks/{user2_task_id}")
    assert access_other_task_response.status_code == 404  # Assuming we return 404 instead of 403 for security

    # Attempt to update another user's task (should fail)
    update_data = {"title": "Attempted update"}
    update_other_task_response = client.put(f"/api/{user1_id}/tasks/{user2_task_id}", json=update_data)
    assert update_other_task_response.status_code == 404  # Assuming we return 404 instead of 403 for security

    # Attempt to delete another user's task (should fail)
    delete_other_task_response = client.delete(f"/api/{user1_id}/tasks/{user2_task_id}")
    assert delete_other_task_response.status_code == 404  # Assuming we return 404 instead of 403 for security


def test_cross_user_access_prevention(client: TestClient, session: Session):
    """
    Additional test to verify that users cannot access each other's tasks
    """
    # Create multiple tasks for user A
    user_a_id = "user-a-id"
    task_a1_data = {
        "title": "User A task 1",
        "description": "First task for user A",
        "user_id": user_a_id
    }
    task_a2_data = {
        "title": "User A task 2",
        "description": "Second task for user A",
        "user_id": user_a_id
    }

    client.post(f"/api/{user_a_id}/tasks", json=task_a1_data)
    client.post(f"/api/{user_a_id}/tasks", json=task_a2_data)

    # Create multiple tasks for user B
    user_b_id = "user-b-id"
    task_b1_data = {
        "title": "User B task 1",
        "description": "First task for user B",
        "user_id": user_b_id
    }
    task_b2_data = {
        "title": "User B task 2",
        "description": "Second task for user B",
        "user_id": user_b_id
    }

    client.post(f"/api/{user_b_id}/tasks", json=task_b1_data)
    client.post(f"/api/{user_b_id}/tasks", json=task_b2_data)

    # Verify user A can only see their own tasks
    user_a_tasks = client.get(f"/api/{user_a_id}/tasks").json()
    assert len(user_a_tasks) == 2
    for task in user_a_tasks:
        assert task["user_id"] == user_a_id

    # Verify user B can only see their own tasks
    user_b_tasks = client.get(f"/api/{user_b_id}/tasks").json()
    assert len(user_b_tasks) == 2
    for task in user_b_tasks:
        assert task["user_id"] == user_b_id
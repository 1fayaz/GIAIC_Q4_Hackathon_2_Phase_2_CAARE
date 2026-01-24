from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import List
from sqlmodel import Session
from src.models.task import Task, TaskCreate, TaskUpdate
from src.schemas.task import TaskResponse
from src.database import get_session
from src.api.deps import get_current_user_dep
from src.services.task_service import TaskService
from src.utils.security import handle_forbidden_access, handle_not_found


router = APIRouter()


@router.get("/tasks", response_model=List[TaskResponse], tags=["tasks"])
async def list_tasks(
    user_id: str = Path(..., description="The ID of the user whose tasks to retrieve"),
    current_user: dict = Depends(get_current_user_dep),
    session: Session = Depends(get_session)
):
    """
    Retrieve all tasks associated with the specified user ID
    """
    # Verify that the user_id in the URL matches the user_id in the JWT token
    if user_id != current_user["user_id"]:
        raise handle_forbidden_access("User ID in URL does not match JWT token")

    # Use TaskService to get tasks for the user
    tasks = TaskService.get_tasks_by_user_id(session, user_id)

    return tasks


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
async def create_task(
    task_data: TaskCreate,
    user_id: str = Path(..., description="The ID of the user creating the task"),
    current_user: dict = Depends(get_current_user_dep),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the specified user
    """
    # Verify that the user_id in the URL matches the user_id in the JWT token
    if user_id != current_user["user_id"]:
        raise handle_forbidden_access("User ID in URL does not match JWT token")

    # Ensure the task is being created for the correct user
    if user_id != task_data.user_id:
        raise handle_forbidden_access("Task user_id does not match URL user_id")

    # Use TaskService to create the task
    task = TaskService.create_task(session, task_data)

    return task


@router.get("/tasks/{id}", response_model=TaskResponse, tags=["tasks"])
async def get_task(
    user_id: str = Path(..., description="The ID of the user who owns the task"),
    id: str = Path(..., description="The ID of the task to retrieve"),
    current_user: dict = Depends(get_current_user_dep),
    session: Session = Depends(get_session)
):
    """
    Retrieve details of a specific task by its ID
    """
    # Verify that the user_id in the URL matches the user_id in the JWT token
    if user_id != current_user["user_id"]:
        raise handle_forbidden_access("User ID in URL does not match JWT token")

    # Use TaskService to get the specific task
    db_task = TaskService.get_task_by_id_and_user(session, id, user_id)

    if not db_task:
        raise handle_not_found("Task")

    return db_task


@router.put("/tasks/{id}", response_model=TaskResponse, tags=["tasks"])
async def update_task(
    task_data: TaskUpdate,
    user_id: str = Path(..., description="The ID of the user who owns the task"),
    id: str = Path(..., description="The ID of the task to update"),
    current_user: dict = Depends(get_current_user_dep),
    session: Session = Depends(get_session)
):
    """
    Update the details of a specific task
    """
    # Verify that the user_id in the URL matches the user_id in the JWT token
    if user_id != current_user["user_id"]:
        raise handle_forbidden_access("User ID in URL does not match JWT token")

    # Use TaskService to get the specific task
    db_task = TaskService.get_task_by_id_and_user(session, id, user_id)

    if not db_task:
        raise handle_not_found("Task")

    # Use TaskService to update the task
    updated_task = TaskService.update_task(session, db_task, task_data)

    return updated_task


@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
async def delete_task(
    user_id: str = Path(..., description="The ID of the user who owns the task"),
    id: str = Path(..., description="The ID of the task to delete"),
    current_user: dict = Depends(get_current_user_dep),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by its ID
    """
    # Verify that the user_id in the URL matches the user_id in the JWT token
    if user_id != current_user["user_id"]:
        raise handle_forbidden_access("User ID in URL does not match JWT token")

    # Use TaskService to get the specific task
    db_task = TaskService.get_task_by_id_and_user(session, id, user_id)

    if not db_task:
        raise handle_not_found("Task")

    # Use TaskService to delete the task
    TaskService.delete_task(session, db_task)

    return


@router.patch("/tasks/{id}/complete", response_model=TaskResponse, tags=["tasks"])
async def toggle_task_completion(
    user_id: str = Path(..., description="The ID of the user who owns the task"),
    id: str = Path(..., description="The ID of the task to toggle"),
    current_user: dict = Depends(get_current_user_dep),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task
    """
    # Verify that the user_id in the URL matches the user_id in the JWT token
    if user_id != current_user["user_id"]:
        raise handle_forbidden_access("User ID in URL does not match JWT token")

    # Use TaskService to get the specific task
    db_task = TaskService.get_task_by_id_and_user(session, id, user_id)

    if not db_task:
        raise handle_not_found("Task")

    # Use TaskService to toggle the completion status
    updated_task = TaskService.toggle_task_completion(session, db_task)

    return updated_task
from typing import List, Optional
from sqlmodel import Session, select
from src.models.task import Task, TaskCreate, TaskUpdate
from src.utils.security import handle_forbidden_access, handle_not_found


class TaskService:
    """
    Service class for handling task-related business logic
    """

    @staticmethod
    def get_tasks_by_user_id(session: Session, user_id: str) -> List[Task]:
        """
        Get all tasks for a specific user
        """
        statement = select(Task).where(Task.user_id == user_id)
        return session.exec(statement).all()

    @staticmethod
    def get_task_by_id_and_user(session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """
        Get a specific task by its ID and user ID
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def create_task(session: Session, task_create: TaskCreate) -> Task:
        """
        Create a new task
        """
        task = Task.model_validate(task_create)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def update_task(session: Session, db_task: Task, task_update: TaskUpdate) -> Task:
        """
        Update a task with the provided data
        """
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(session: Session, db_task: Task) -> bool:
        """
        Delete a task
        """
        session.delete(db_task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(session: Session, db_task: Task) -> Task:
        """
        Toggle the completion status of a task
        """
        db_task.completed = not db_task.completed
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def verify_user_owns_task(task: Task, user_id: str) -> bool:
        """
        Verify that the user owns the task
        """
        return task.user_id == user_id
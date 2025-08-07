from fastapi import Depends, APIRouter, HTTPException
from typing import Optional, List
from app.api.dependencies.auth import get_current_user
from app.infrastructure.database.models.user import User
from app.services.task_service import task_service
from app.domain.schemas.task import (
    TaskListCreate,
    TaskCreate,
    TaskUpdate,
    TaskListOut,
    TaskOut,
)


router = APIRouter(prefix="/task", tags=["Task"])


@router.post("/lists", status_code=201, response_model=TaskListOut)
async def create_list(
    data: TaskListCreate, current_user: User = Depends(get_current_user)
) -> TaskListOut:
    """
    Create a new task list.

    Args:
        data (TaskListCreate): Payload with the name of the list.

    Returns:
        dict: The created task list object.
    """
    return await task_service.create_list(data)


@router.get("/lists", response_model=List[TaskListOut])
async def get_lists(current_user: User = Depends(get_current_user)) -> List[dict]:
    """
    Retrieve all task lists with their completion percentage.

    Returns:
        List[dict]: A list of task lists with metadata.
    """
    return await task_service.get_all_lists()


@router.get("/lists/{list_id}", response_model=TaskListOut)
async def get_list(
    list_id: int, current_user: User = Depends(get_current_user)
) -> TaskListOut:
    """
    Get a specific task list by ID, including completion percentage.

    Args:
        list_id (int): The ID of the task list.

    Returns:
        dict: Task list details with tasks and completion percentage.

    Raises:
        HTTPException: 404 if the list is not found.
    """
    result = await task_service.get_list_with_progress(list_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task list not found")
    return result


@router.post("/lists/{list_id}/tasks", status_code=201, response_model=TaskOut)
async def create_task(
    list_id: int, task: TaskCreate, current_user: User = Depends(get_current_user)
) -> TaskOut:
    """
    Create a new task inside a given task list.

    Args:
        list_id (int): The ID of the parent task list.
        task (TaskCreate): Task data (title, description, priority, etc.)

    Returns:
        dict: The created task object.

    Raises:
        HTTPException: 404 if the task list does not exist.
    """
    return await task_service.create_task(list_id, task)


@router.get("/lists/{list_id}/tasks", response_model=List[TaskOut])
async def list_tasks(
    list_id: int,
    completed: Optional[bool] = None,
    priority: Optional[int] = None,
    current_user: User = Depends(get_current_user),
) -> List[TaskOut]:
    """
    List tasks in a given list, with optional filters by completion and priority.

    Args:
        list_id (int): The ID of the task list.
        completed (bool, optional): Filter by task completion status.
        priority (int, optional): Filter by task priority (1-5).

    Returns:
        List[dict]: Filtered list of tasks.
    """
    return await task_service.list_tasks(list_id, completed, priority)


@router.patch("/tasks/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: int, data: TaskUpdate, current_user: User = Depends(get_current_user)
) -> TaskOut:
    """
    Update an existing task by ID.

    Args:
        task_id (int): The ID of the task.
        data (TaskUpdate): Fields to update (title, completed, etc.)

    Returns:
        dict: The updated task object.

    Raises:
        HTTPException: 404 if the task does not exist.
    """
    task = await task_service.update_task(task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}", status_code=200)
async def delete_task(
    task_id: int, current_user: User = Depends(get_current_user)
) -> dict:
    """
    Delete a task by ID.

    Args:
        task_id (int): The ID of the task to delete.

    Returns:
        dict: A message confirming deletion.

    Raises:
        HTTPException: 404 if the task does not exist.
    """
    return await task_service.delete_task(task_id)

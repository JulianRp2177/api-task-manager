from fastapi import Depends
from app.api.dependencies.auth import get_current_user
from app.infrastructure.database.models.user import User

from fastapi import APIRouter
from app.domain.schemas.assigned_task import AssignTask
from app.services.assigned_task_service import assigned_task_service

router = APIRouter(prefix="/assigned_task", tags=["Assigned_task"])


@router.post("/{task_id}")
async def assign_task(
    task_id: int, payload: AssignTask, current_user: User = Depends(get_current_user)
) -> dict:
    """
    Assign a task to an existing user by email.

    Args:
        task_id (int): The ID of the task to be assigned.
        payload (AssignTask): The payload containing the user's email.

    Returns:
        dict: A message indicating the task was successfully assigned.

    Raises:
        HTTPException:
            - 404 if the task or user is not found.
    """
    return await assigned_task_service.assign_user_to_task(task_id, payload)

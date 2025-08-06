from fastapi import HTTPException
from app.infrastructure.database.repositories.task_repo import task_repo
from app.infrastructure.database.repositories.user_repo import user_repo
from app.domain.schemas.assigned_task import AssignTask
from app.utils.send_email import simulate_task_assignment_email
from app.core.logging import get_logging

log = get_logging(__name__)


class AssignedTaskService:
    def __init__(self):
        self.task_repo = task_repo
        self.user_repo = user_repo

    async def assign_user_to_task(self, task_id: int, payload: AssignTask):
        task = await self.task_repo.get_task(task_id)
        if not task:
            raise HTTPException(404, "Task not found")

        user = await self.user_repo.get_by_email(payload.user_email)
        if not user:
            raise HTTPException(404, "User not found")

        task = await self.task_repo.assign_user_to_task(task, user)
        if not task:
            raise HTTPException(500, "Failed to assign user to task")
        await simulate_task_assignment_email(user.email, task.title)

        return {"message": f"Task assigned to {user.email}"}


assigned_task_service = AssignedTaskService()

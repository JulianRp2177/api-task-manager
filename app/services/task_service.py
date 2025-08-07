from fastapi import HTTPException
from app.infrastructure.database.repositories.task_repo import task_repo
from app.domain.schemas.task import (
    TaskListCreate,
    TaskCreate,
    TaskUpdate,
    TaskListOut,
    TaskOut,
)


class TaskService:
    def __init__(self):
        self.repo = task_repo

    async def create_list(self, payload: TaskListCreate):
        list_created = await self.repo.create_list(payload.name)
        list_dict = {
            "id": list_created.id,
            "name": list_created.name,
            "created_at": list_created.created_at,
            "tasks": [],
            "completed_percentage": 0.0,
        }
        return TaskListOut.model_validate(list_dict)

    async def get_list_with_progress(self, list_id: int) -> TaskListOut:
        task_list = await self.repo.get_list(list_id)
        if not task_list:
            return None

        total = len(task_list.tasks)
        done = sum(1 for item in task_list.tasks if item.completed)
        percent = round((done / total * 100), 2) if total else 0

        return TaskListOut(
            id=task_list.id,
            name=task_list.name,
            created_at=task_list.created_at,
            tasks=[TaskOut.model_validate(task) for task in task_list.tasks],
            completed_percentage=percent,
        )

    async def get_all_lists(self):
        lists = await self.repo.get_all_lists()
        return [await self.get_list_with_progress(task_list.id) for task_list in lists]

    async def create_task(self, list_id: int, payload: TaskCreate):
        task_list = await self.repo.get_list(list_id)
        if not task_list:
            raise HTTPException(status_code=404, detail="Task list not found")

        task = await self.repo.create_task(list_id, payload.model_dump())
        return TaskOut.model_validate(task)

    async def list_tasks(self, list_id: int, completed=None, priority=None):
        return await self.repo.list_tasks(list_id, completed, priority)

    async def update_task(self, task_id: int, payload: TaskUpdate):
        task = await self.repo.get_task(task_id)
        if not task:
            return None
        return await self.repo.update_task(task, payload.dict(exclude_unset=True))

    async def delete_task(self, task_id: int):
        deleted = await self.repo.delete_task(task_id)
        if not deleted:
            raise HTTPException(404, "Task not found")
        return {"message": "Task deleted successfully"}


task_service = TaskService()

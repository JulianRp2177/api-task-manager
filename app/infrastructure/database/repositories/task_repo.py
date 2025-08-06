from tortoise.expressions import Q
from app.infrastructure.database.models.task import Task, TaskList
from typing import Optional


class TaskRepository:
    async def create_list(self, name: str) -> TaskList:
        return await TaskList.create(name=name)

    async def get_list(self, list_id: int) -> Optional[TaskList]:
        obj = await TaskList.get_or_none(id=list_id)
        if obj:
            await obj.fetch_related("tasks")
        return obj

    async def get_all_lists(self) -> list[TaskList]:
        return await TaskList.all()

    async def create_task(self, list_id: int, data: dict) -> Task:
        return await Task.create(task_list_id=list_id, **data)

    async def list_tasks(
        self, list_id: int, completed=None, priority=None
    ) -> list[Task]:
        filters = Q(task_list_id=list_id)
        if completed is not None:
            filters &= Q(completed=completed)
        if priority is not None:
            filters &= Q(priority=priority)
        return await Task.filter(filters)

    async def get_task(self, task_id: int) -> Optional[Task]:
        return await Task.get_or_none(id=task_id)

    async def update_task(self, task: Task, data: dict):
        task.update_from_dict(data)
        await task.save()
        return task

    async def delete_task(self, task_id: int):
        return await Task.filter(id=task_id).delete()

    async def assign_user_to_task(self, task: Task, user) -> Task:
        task.assigned_to = user
        await task.save()
        return task


task_repo = TaskRepository()

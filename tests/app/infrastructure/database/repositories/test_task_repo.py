import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.infrastructure.database.repositories.task_repo import TaskRepository

pytestmark = pytest.mark.asyncio


class TestTaskRepository:

    @patch("app.infrastructure.database.repositories.task_repo.TaskList", autospec=True)
    async def test_create_list_success(self, mock_tasklist_class):
        repo = TaskRepository()
        mock_instance = MagicMock()
        mock_tasklist_class.create = AsyncMock(return_value=mock_instance)

        result = await repo.create_list("Test List")

        mock_tasklist_class.create.assert_awaited_once_with(name="Test List")
        assert result == mock_instance

    @patch("app.infrastructure.database.repositories.task_repo.Task", autospec=True)
    async def test_create_task_success(self, mock_task_class):
        repo = TaskRepository()
        mock_instance = MagicMock()
        mock_task_class.create = AsyncMock(return_value=mock_instance)

        data = {"title": "Task", "description": "Test", "priority": 3}
        result = await repo.create_task(1, data)

        mock_task_class.create.assert_awaited_once_with(task_list_id=1, **data)
        assert result == mock_instance

    @patch("app.infrastructure.database.repositories.task_repo.Task", autospec=True)
    async def test_list_tasks_success(self, mock_task_class):
        repo = TaskRepository()
        mock_task_class.filter = AsyncMock(return_value=["task1", "task2"])

        result = await repo.list_tasks(1, completed=True, priority=3)

        mock_task_class.filter.assert_awaited_once()
        assert result == ["task1", "task2"]

    @patch("app.infrastructure.database.repositories.task_repo.Task", autospec=True)
    async def test_get_task_success(self, mock_task_class):
        repo = TaskRepository()
        mock_task_class.get_or_none = AsyncMock(return_value="task")

        result = await repo.get_task(1)

        mock_task_class.get_or_none.assert_awaited_once_with(id=1)
        assert result == "task"

    @patch("app.infrastructure.database.repositories.task_repo.Task", autospec=True)
    async def test_update_task_success(self, mock_task_class):
        repo = TaskRepository()
        task_instance = MagicMock()
        task_instance.save = AsyncMock()

        result = await repo.update_task(task_instance, {"title": "Updated"})

        task_instance.update_from_dict.assert_called_once_with({"title": "Updated"})
        task_instance.save.assert_awaited_once()
        assert result == task_instance

    @patch("app.infrastructure.database.repositories.task_repo.Task", autospec=True)
    async def test_delete_task_success(self, mock_task_class):
        repo = TaskRepository()
        mock_task_class.filter.return_value.delete = AsyncMock(return_value=1)

        result = await repo.delete_task(1)

        mock_task_class.filter.assert_called_once_with(id=1)
        mock_task_class.filter.return_value.delete.assert_awaited_once()
        assert result == 1

    @patch("app.infrastructure.database.repositories.task_repo.Task", autospec=True)
    async def test_assign_user_to_task_success(self, mock_task_class):
        repo = TaskRepository()
        task_instance = MagicMock()
        task_instance.save = AsyncMock()
        mock_user = MagicMock()

        result = await repo.assign_user_to_task(task_instance, mock_user)

        assert task_instance.assigned_to == mock_user
        task_instance.save.assert_awaited_once()
        assert result == task_instance

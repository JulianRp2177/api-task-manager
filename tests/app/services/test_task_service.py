import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime
from app.services.task_service import TaskService
from app.domain.schemas.task import TaskCreate, TaskUpdate

pytestmark = pytest.mark.asyncio


class TestTaskService:

    @patch("app.services.task_service.task_repo")
    async def test_create_list_success(self, mock_repo):
        from app.domain.schemas.task import TaskListCreate

        mock_list = MagicMock()
        mock_list.id = 1
        mock_list.name = "Test List"
        mock_list.created_at = datetime.utcnow()

        mock_repo.create_list = AsyncMock(return_value=mock_list)

        service = TaskService()
        result = await service.create_list(TaskListCreate(name="Test List"))

        assert result.name == "Test List"

    @patch("app.services.task_service.task_repo")
    async def test_get_list_with_progress_success(self, mock_repo):
        from app.domain.schemas.task import TaskOut

        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Task"
        mock_task.description = "desc"
        mock_task.priority = 2
        mock_task.completed = True
        mock_task.created_at = datetime.utcnow()

        mock_list = MagicMock()
        mock_list.id = 1
        mock_list.name = "List"
        mock_list.created_at = datetime.utcnow()
        mock_list.tasks = [mock_task]

        mock_repo.get_list = AsyncMock(return_value=mock_list)

        service = TaskService()
        result = await service.get_list_with_progress(1)

        assert result.name == "List"
        assert result.completed_percentage == 100.0
        assert isinstance(result.tasks[0], TaskOut)

    @patch("app.services.task_service.task_repo")
    async def test_create_task_success(self, mock_repo):
        mock_task = MagicMock(
            id=1,
            title="Task",
            description="desc",
            priority=1,
            completed=False,
            created_at=datetime.utcnow(),
        )
        mock_list = MagicMock()
        mock_repo.get_list = AsyncMock(return_value=mock_list)
        mock_repo.create_task = AsyncMock(return_value=mock_task)

        service = TaskService()
        result = await service.create_task(1, TaskCreate(title="Task"))

        assert result.title == "Task"

    @patch("app.services.task_service.task_repo")
    async def test_update_task_success(self, mock_repo):
        mock_task = MagicMock()
        mock_task.update_from_dict = MagicMock()
        mock_task.save = AsyncMock()

        mock_repo.get_task = AsyncMock(return_value=mock_task)
        mock_repo.update_task = AsyncMock(return_value=mock_task)

        service = TaskService()
        result = await service.update_task(1, TaskUpdate(title="Updated"))

        assert result is not None

    @patch("app.services.task_service.task_repo")
    async def test_update_task_not_found(self, mock_repo):
        mock_repo.get_task = AsyncMock(return_value=None)

        service = TaskService()
        result = await service.update_task(1, TaskUpdate(title="Updated"))

        assert result is None

    @patch("app.services.task_service.task_repo")
    async def test_delete_task_success(self, mock_repo):
        mock_repo.delete_task = AsyncMock(return_value=1)

        service = TaskService()
        result = await service.delete_task(1)

        assert result["message"] == "Task deleted successfully"

    @patch("app.services.task_service.task_repo")
    async def test_delete_task_not_found(self, mock_repo):
        mock_repo.delete_task = AsyncMock(return_value=0)

        service = TaskService()
        with pytest.raises(Exception) as exc:
            await service.delete_task(1)

        assert exc.value.status_code == 404

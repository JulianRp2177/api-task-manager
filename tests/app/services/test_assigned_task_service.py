import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from app.services.assigned_task_service import AssignedTaskService
from app.domain.schemas.assigned_task import AssignTask

pytestmark = pytest.mark.asyncio


class TestAssignedTaskService:

    @patch(
        "app.services.assigned_task_service.simulate_task_assignment_email",
        new_callable=AsyncMock,
    )
    @patch("app.services.assigned_task_service.task_repo")
    @patch("app.services.assigned_task_service.user_repo")
    async def test_assign_user_to_task_success(
        self, mock_user_repo, mock_task_repo, mock_email
    ):
        service = AssignedTaskService()
        payload = AssignTask(user_email="test@example.com")

        mock_task_repo.get_task = AsyncMock(return_value=MagicMock())
        mock_user_repo.get_by_email = AsyncMock(
            return_value=MagicMock(email="test@example.com")
        )
        mock_task_repo.assign_user_to_task = AsyncMock(
            return_value=MagicMock(title="Task title")
        )

        result = await service.assign_user_to_task(1, payload)

        assert result == {"message": "Task assigned to test@example.com"}
        mock_email.assert_awaited_once_with("test@example.com", "Task title")

    @patch("app.services.assigned_task_service.task_repo")
    async def test_assign_user_to_task_task_not_found(self, mock_task_repo):
        service = AssignedTaskService()
        payload = AssignTask(user_email="test@example.com")

        mock_task_repo.get_task = AsyncMock(return_value=None)

        with pytest.raises(HTTPException) as exc:
            await service.assign_user_to_task(1, payload)

        assert exc.value.status_code == 404
        assert exc.value.detail == "Task not found"

    @patch("app.services.assigned_task_service.task_repo")
    @patch("app.services.assigned_task_service.user_repo")
    async def test_assign_user_to_task_user_not_found(
        self, mock_user_repo, mock_task_repo
    ):
        service = AssignedTaskService()
        payload = AssignTask(user_email="test@example.com")

        mock_task_repo.get_task = AsyncMock(return_value=MagicMock())
        mock_user_repo.get_by_email = AsyncMock(return_value=None)

        with pytest.raises(HTTPException) as exc:
            await service.assign_user_to_task(1, payload)

        assert exc.value.status_code == 404
        assert exc.value.detail == "User not found"

    @patch("app.services.assigned_task_service.task_repo")
    @patch("app.services.assigned_task_service.user_repo")
    async def test_assign_user_to_task_assign_failed(
        self, mock_user_repo, mock_task_repo
    ):
        service = AssignedTaskService()
        payload = AssignTask(user_email="test@example.com")

        mock_task_repo.get_task = AsyncMock(return_value=MagicMock())
        mock_user_repo.get_by_email = AsyncMock(return_value=MagicMock())
        mock_task_repo.assign_user_to_task = AsyncMock(return_value=None)

        with pytest.raises(HTTPException) as exc:
            await service.assign_user_to_task(1, payload)

        assert exc.value.status_code == 500
        assert exc.value.detail == "Failed to assign user to task"

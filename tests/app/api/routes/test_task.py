import pytest
from datetime import datetime
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from app.main import app

BASE_URL = "/task"


class TestTaskEndpoints:
    mock_user = AsyncMock(
        id=1,
        email="test@example.com",
        full_name="Test User",
        is_active=True,
        hashed_password="mock_hashed_password",
    )

    list_out = {
        "id": 1,
        "name": "My List",
        "created_at": datetime.utcnow().isoformat(),
        "tasks": [],
        "completed_percentage": 0.0,
    }

    task_out = {
        "id": 1,
        "title": "New Task",
        "description": "Sample",
        "priority": 3,
        "completed": False,
        "created_at": datetime.utcnow().isoformat(),
        "task_list_id": 1,
    }

    def setup_mock_user(self, mock_get_user):
        mock_get_user.return_value = self.mock_user

    @pytest.mark.asyncio
    @patch("app.api.routes.task.get_current_user", new_callable=AsyncMock)
    @patch("app.services.task_service.task_service.create_list", new_callable=AsyncMock)
    async def test_create_list_success(self, mock_create_list, mock_get_user):
        self.setup_mock_user(mock_get_user)
        mock_create_list.return_value = self.list_out

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                f"{BASE_URL}/lists",
                json={"name": "My List"},
                headers={"Authorization": "Bearer mocktoken"},
            )

        assert response.status_code == 201
        assert response.json()["name"] == "My List"

    @pytest.mark.asyncio
    @patch("app.api.routes.task.get_current_user", new_callable=AsyncMock)
    @patch(
        "app.services.task_service.task_service.get_all_lists",
        new_callable=AsyncMock,
    )
    async def test_get_all_lists_success(self, mock_get_all_lists, mock_get_user):
        self.setup_mock_user(mock_get_user)
        mock_get_all_lists.return_value = [self.list_out]

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f"{BASE_URL}/lists", headers={"Authorization": "Bearer mocktoken"}
            )

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert response.json()[0]["name"] == "My List"

    @pytest.mark.asyncio
    @patch("app.api.routes.task.get_current_user", new_callable=AsyncMock)
    @patch(
        "app.services.task_service.task_service.get_list_with_progress",
        new_callable=AsyncMock,
    )
    async def test_get_single_list_success(self, mock_get_list, mock_get_user):
        self.setup_mock_user(mock_get_user)
        mock_get_list.return_value = self.list_out

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f"{BASE_URL}/lists/1", headers={"Authorization": "Bearer mocktoken"}
            )

        assert response.status_code == 200
        assert response.json()["name"] == "My List"

    @pytest.mark.asyncio
    @patch("app.api.routes.task.get_current_user", new_callable=AsyncMock)
    @patch(
        "app.services.task_service.task_service.get_list_with_progress",
        new_callable=AsyncMock,
    )
    async def test_get_single_list_not_found(self, mock_get_list, mock_get_user):
        self.setup_mock_user(mock_get_user)
        mock_get_list.return_value = None

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f"{BASE_URL}/lists/99", headers={"Authorization": "Bearer mocktoken"}
            )

        assert response.status_code == 404

    @pytest.mark.asyncio
    @patch("app.api.routes.task.get_current_user", new_callable=AsyncMock)
    @patch("app.services.task_service.task_service.create_task", new_callable=AsyncMock)
    async def test_create_task_success(self, mock_create_task, mock_get_user):
        self.setup_mock_user(mock_get_user)
        mock_create_task.return_value = self.task_out

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                f"{BASE_URL}/lists/1/tasks",
                json={"title": "New Task", "description": "Sample", "priority": 3},
                headers={"Authorization": "Bearer mocktoken"},
            )

        assert response.status_code == 201
        assert response.json()["title"] == "New Task"

    @pytest.mark.asyncio
    @patch("app.api.routes.task.get_current_user", new_callable=AsyncMock)
    @patch("app.services.task_service.task_service.update_task", new_callable=AsyncMock)
    async def test_update_task_success(self, mock_update_task, mock_get_user):
        self.setup_mock_user(mock_get_user)
        mock_update_task.return_value = {
            **self.task_out,
            "title": "Updated Task",
            "completed": True,
        }

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.patch(
                f"{BASE_URL}/tasks/1",
                json={"title": "Updated Task", "completed": True},
                headers={"Authorization": "Bearer mocktoken"},
            )

        assert response.status_code == 200
        assert response.json()["title"] == "Updated Task"

    @pytest.mark.asyncio
    @patch("app.api.routes.task.get_current_user", new_callable=AsyncMock)
    @patch("app.services.task_service.task_service.delete_task", new_callable=AsyncMock)
    async def test_delete_task_success(self, mock_delete_task, mock_get_user):
        self.setup_mock_user(mock_get_user)
        mock_delete_task.return_value = {"message": "Task deleted successfully"}

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.delete(
                f"{BASE_URL}/tasks/1", headers={"Authorization": "Bearer mocktoken"}
            )

        assert response.status_code == 200
        assert response.json()["message"] == "Task deleted successfully"

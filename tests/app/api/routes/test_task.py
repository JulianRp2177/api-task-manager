import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.routes import task
from app.infrastructure.database.models.user import User
from unittest.mock import AsyncMock, patch

client = TestClient(app)


def mock_get_current_user():
    return User(id=1, username="testuser", email="test@example.com")


@pytest.fixture(autouse=True)
def override_get_current_user():
    app.dependency_overrides[task.get_current_user] = mock_get_current_user
    yield
    app.dependency_overrides = {}


@patch("app.api.routes.task.task_service.create_list", new_callable=AsyncMock)
def test_create_list(mock_create_list):
    # Given
    mock_create_list.return_value = {
        "id": 1,
        "name": "My list",
        "created_at": "2025-08-07T14:03:19.297759Z",
        "tasks": [],
        "completed_percentage": 0,
    }

    payload = {"name": "My list"}
    # When
    response = client.post("/api/task/lists", json=payload)
    # Then
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My list"
    assert data["id"] == 1

    mock_create_list.assert_awaited_once()


@patch("app.api.routes.task.task_service.get_all_lists", new_callable=AsyncMock)
def test_get_lists(mock_get_all_lists):
    mock_get_all_lists.return_value = [
        {
            "id": 1,
            "name": "job",
            "created_at": "2025-08-06T18:30:37.097015Z",
            "tasks": [
                {
                    "id": 1,
                    "title": "programmer",
                    "description": "vscode",
                    "priority": 1,
                    "completed": False,
                    "created_at": "2025-08-06T18:40:29.889838Z",
                }
            ],
            "completed_percentage": 0,
        },
        {
            "id": 2,
            "name": "test",
            "created_at": "2025-08-07T13:55:39.476064Z",
            "tasks": [],
            "completed_percentage": 0,
        },
    ]

    response = client.get("/api/task/lists")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


@patch(
    "app.api.routes.task.task_service.get_list_with_progress", new_callable=AsyncMock
)
def test_get_list_success(mock_get_list):
    mock_get_list.return_value = {
        "id": 1,
        "name": "test",
        "created_at": "2025-08-07T13:55:39.476064Z",
        "tasks": [],
        "completed_percentage": 0,
    }

    response = client.get("/api/task/lists/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@patch(
    "app.api.routes.task.task_service.get_list_with_progress", new_callable=AsyncMock
)
def test_get_list_not_found(mock_get_list):
    mock_get_list.return_value = None

    response = client.get("/api/task/lists/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task list not found"


@patch("app.api.routes.task.task_service.create_task", new_callable=AsyncMock)
def test_create_task(mock_create_task):
    mock_create_task.return_value = {
        "id": 4,
        "title": "Write tests",
        "description": "c-test",
        "priority": 2,
        "completed": False,
        "created_at": "2025-08-07T14:03:45.311669Z",
    }

    payload = {"title": "Write tests", "description": "c-test", "priority": 2}

    response = client.post("/api/task/lists/1/tasks", json=payload)
    assert response.status_code == 201
    assert response.json()["title"] == "Write tests"


@patch("app.api.routes.task.task_service.list_tasks", new_callable=AsyncMock)
def test_list_tasks(mock_list_tasks):
    mock_list_tasks.return_value = [
        {
            "id": 4,
            "title": "test",
            "description": "c-test",
            "priority": 2,
            "completed": False,
            "created_at": "2025-08-07T14:03:45.311669Z",
        },
        {
            "id": 5,
            "title": "test",
            "description": "c-test",
            "priority": 1,
            "completed": False,
            "created_at": "2025-08-07T14:03:45.311669Z",
        },
    ]

    response = client.get("/api/task/lists/1/tasks?completed=true&priority=2")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@patch("app.api.routes.task.task_service.update_task", new_callable=AsyncMock)
def test_update_task_success(mock_update_task):
    mock_update_task.return_value = {
        "id": 5,
        "title": "Updated title",
        "description": "test",
        "completed": True,
        "priority": 3,
        "created_at": "2025-08-07T15:16:47.489Z",
    }

    payload = {
        "title": "Updated title",
        "description": "test",
        "completed": True,
        "priority": 3,
    }

    response = client.patch("/api/task/tasks/5", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"


@patch("app.api.routes.task.task_service.update_task", new_callable=AsyncMock)
def test_update_task_not_found(mock_update_task):
    mock_update_task.return_value = None

    response = client.patch("/api/task/tasks/999", json={"title": "Doesn't matter"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


@patch("app.api.routes.task.task_service.delete_task", new_callable=AsyncMock)
def test_delete_task(mock_delete_task):
    mock_delete_task.return_value = {"message": "Task deleted successfully"}

    response = client.delete("/api/task/tasks/5")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"

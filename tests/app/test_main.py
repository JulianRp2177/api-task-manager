import pytest
from fastapi.testclient import TestClient
from app.main import create_application


@pytest.mark.asyncio
async def test_application_lifespan(monkeypatch):
    called = {"init_db": False}

    async def mock_init_db(app):
        called["init_db"] = True

    monkeypatch.setattr("app.main.init_db", mock_init_db)

    app = create_application()

    with TestClient(app) as client:
        response = client.get("/docs")
        assert response.status_code in [200, 404]

    assert called["init_db"] is True

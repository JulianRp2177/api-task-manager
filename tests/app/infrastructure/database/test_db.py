import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from app.infrastructure.database.db import init_db
from app.core.config import settings


@pytest.mark.asyncio
@patch(
    "app.infrastructure.database.db.Tortoise.generate_schemas",
    new_callable=AsyncMock,
)
@patch("app.infrastructure.database.db.Tortoise.init", new_callable=AsyncMock)
async def test_init_db_calls_tortoise_methods(mock_init, mock_generate_schemas):
    app = FastAPI()

    await init_db(app)

    mock_init.assert_awaited_once_with(
        db_url=settings.DATABASE_URL,
        modules={
            "models": [
                "app.infrastructure.database.models.user",
                "app.infrastructure.database.models.task",
            ]
        },
    )
    mock_generate_schemas.assert_awaited_once()

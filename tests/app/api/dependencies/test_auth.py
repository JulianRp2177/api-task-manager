import pytest
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from unittest.mock import AsyncMock, patch
from app.api.dependencies.auth import get_current_user
from app.core.config import settings
from app.infrastructure.database.models.user import User


def generate_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=30)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@pytest.mark.asyncio
@patch("app.api.dependencies.auth.User.get_or_none", new_callable=AsyncMock)
async def test_get_current_user_success(mock_get_user):
    token = generate_token("test@example.com")
    mock_user = User()
    mock_user.email = "test@example.com"
    mock_user.is_active = True
    mock_get_user.return_value = mock_user

    user = await get_current_user(token=token)
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token="invalid.token.here")

    assert exc_info.value.status_code == 401
    assert "Could not validate credentials" in str(exc_info.value.detail)


@pytest.mark.asyncio
@patch("app.api.dependencies.auth.User.get_or_none", new_callable=AsyncMock)
async def test_get_current_user_user_not_found(mock_get_user):
    token = generate_token("test@example.com")
    mock_get_user.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=token)

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
@patch("app.api.dependencies.auth.User.get_or_none", new_callable=AsyncMock)
async def test_get_current_user_user_inactive(mock_get_user):
    token = generate_token("test@example.com")
    mock_user = User()
    mock_user.email = "test@example.com"
    mock_user.is_active = False
    mock_get_user.return_value = mock_user

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=token)

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_token_missing_sub():

    expire = datetime.utcnow() + timedelta(minutes=30)
    token = jwt.encode(
        {"exp": expire},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=token)

    assert exc_info.value.status_code == 401
    assert "Could not validate credentials" in str(exc_info.value.detail)

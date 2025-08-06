import pytest
from unittest.mock import AsyncMock, patch
from app.infrastructure.database.repositories.user_repo import UserRepository

pytestmark = pytest.mark.asyncio


class TestUserRepository:

    @patch("app.infrastructure.database.repositories.user_repo.User", autospec=True)
    async def test_get_by_email_found(self, mock_user_class):
        repo = UserRepository()

        mock_user = AsyncMock()
        mock_user_class.get_or_none = AsyncMock(return_value=mock_user)

        result = await repo.get_by_email("test@example.com")

        mock_user_class.get_or_none.assert_awaited_once_with(email="test@example.com")
        assert result == mock_user

    @patch("app.infrastructure.database.repositories.user_repo.User", autospec=True)
    async def test_get_by_email_not_found(self, mock_user_class):
        repo = UserRepository()

        mock_user_class.get_or_none = AsyncMock(return_value=None)

        result = await repo.get_by_email("notfound@example.com")

        mock_user_class.get_or_none.assert_awaited_once_with(
            email="notfound@example.com"
        )

        assert result is None

    @patch("app.infrastructure.database.repositories.user_repo.User", autospec=True)
    async def test_create_user_success(self, mock_user_class):
        repo = UserRepository()

        mock_user_instance = AsyncMock()
        mock_user_class.create = AsyncMock(return_value=mock_user_instance)

        result = await repo.create("new@example.com", "hashedpassword123")

        mock_user_class.create.assert_awaited_once_with(
            email="new@example.com", hashed_password="hashedpassword123"
        )
        assert result == mock_user_instance

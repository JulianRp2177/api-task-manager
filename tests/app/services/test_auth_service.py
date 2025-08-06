import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import AuthService
from app.domain.schemas.user import UserCreate


@pytest.mark.asyncio
class TestAuthService:

    @patch("app.services.auth_service.user_repo")
    @patch("app.services.auth_service.hash_password", return_value="hashed_pass")
    async def test_register_user_success(self, mock_hash_password, mock_user_repo):
        mock_user_repo.get_by_email = AsyncMock(return_value=None)
        mock_user_repo.create = AsyncMock(
            return_value=MagicMock(email="test@example.com")
        )

        service = AuthService()
        user_data = UserCreate(
            email="test@example.com", password="123456", full_name="Test User"
        )
        result = await service.register_user(user_data)

        assert result.email == "test@example.com"
        mock_user_repo.create.assert_awaited_once_with(
            "test@example.com", "hashed_pass"
        )

    @patch("app.services.auth_service.user_repo")
    async def test_register_user_email_exists(self, mock_user_repo):
        mock_user_repo.get_by_email = AsyncMock(return_value=MagicMock())

        service = AuthService()
        user_data = UserCreate(
            email="test@example.com", password="123456", full_name="Test User"
        )

        with pytest.raises(HTTPException) as exc:
            await service.register_user(user_data)
        assert exc.value.status_code == 400
        assert exc.value.detail == "Email already registered"

    @patch("app.services.auth_service.user_repo")
    @patch("app.services.auth_service.verify_password", return_value=True)
    @patch("app.services.auth_service.create_access_token", return_value="token123")
    async def test_login_user_success(self, mock_token, mock_verify, mock_user_repo):
        user = MagicMock(email="test@example.com", hashed_password="hashed")
        mock_user_repo.get_by_email = AsyncMock(return_value=user)

        form_data = OAuth2PasswordRequestForm(
            username="test@example.com",
            password="123456",
            scope="",
            grant_type="",
            client_id=None,
            client_secret=None,
        )

        service = AuthService()
        result = await service.login_user(form_data)

        assert result["access_token"] == "token123"
        assert result["token_type"] == "bearer"
        mock_verify.assert_called_once_with("123456", "hashed")

    @patch("app.services.auth_service.user_repo")
    @patch("app.services.auth_service.verify_password", return_value=False)
    async def test_login_user_invalid_credentials(self, mock_verify, mock_user_repo):
        user = MagicMock(email="test@example.com", hashed_password="hashed")
        mock_user_repo.get_by_email = AsyncMock(return_value=user)

        form_data = OAuth2PasswordRequestForm(
            username="test@example.com",
            password="wrongpass",
            scope="",
            grant_type="",
            client_id=None,
            client_secret=None,
        )

        service = AuthService()

        with pytest.raises(HTTPException) as exc:
            await service.login_user(form_data)
        assert exc.value.status_code == 401
        assert exc.value.detail == "Invalid credentials"

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from jose import jwt
from app.core.config import settings


class TestSecurityUtils:

    def test_hash_and_verify_password(self):
        password = "securepassword"
        hashed = hash_password(password)

        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False

    def test_create_access_token_default_expiry(self):
        data = {"sub": "user@example.com"}
        token = create_access_token(data)

        decoded = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        assert decoded["sub"] == "user@example.com"
        assert "exp" in decoded

    def test_create_access_token_custom_expiry(self):
        data = {"sub": "user@example.com"}
        expires_delta = 1
        token = create_access_token(data, expires_delta=expires_delta)

        decoded = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        assert decoded["sub"] == "user@example.com"
        assert isinstance(decoded["exp"], int)

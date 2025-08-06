from fastapi import HTTPException
from app.core.security import hash_password, verify_password, create_access_token
from app.infrastructure.database.repositories.user_repo import user_repo
from app.domain.schemas.user import UserCreate
from fastapi.security import OAuth2PasswordRequestForm


class AuthService:
    def __init__(self):
        self.user_repo = user_repo

    async def register_user(self, user: UserCreate):
        exists = await self.user_repo.get_by_email(user.email)
        if exists:
            raise HTTPException(400, "Email already registered")
        return await self.user_repo.create(user.email, hash_password(user.password))

    async def login_user(self, form_data: OAuth2PasswordRequestForm):
        user_obj = await self.user_repo.get_by_email(form_data.username)
        is_valid = user_obj and verify_password(
            form_data.password, user_obj.hashed_password
        )
        if not is_valid:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"sub": user_obj.email})
        return {"access_token": token, "token_type": "bearer"}


auth_service = AuthService()

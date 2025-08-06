from app.infrastructure.database.models.user import User


class UserRepository:
    async def get_by_email(self, email: str) -> User | None:
        return await User.get_or_none(email=email)

    async def create(self, email: str, hashed_password: str) -> User:
        return await User.create(email=email, hashed_password=hashed_password)


user_repo = UserRepository()

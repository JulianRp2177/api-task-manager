from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    WEB_APP_TITLE: str = "Task Manager API"
    WEB_APP_DESCRIPTION: str = "REST API for the assignment of tasks."
    WEB_APP_VERSION: str = "1.0.0"
    DEBUGGER: bool = True
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()

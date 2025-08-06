from fastapi import FastAPI
from app.infrastructure.database.db import init_db
from contextlib import asynccontextmanager
from app.api.routes import auth, task, assigned_task
from app.core.logging import get_logging
from app.core.config import settings
from app.debugger import initialize_fastapi_server_debugger_if_needed

log = get_logging(__name__)

if settings.DEBUGGER:
    initialize_fastapi_server_debugger_if_needed()


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting app...")
    await init_db(app)
    yield
    log.info("Shutting down...")


def create_application() -> FastAPI:

    app = FastAPI(
        title=settings.WEB_APP_TITLE,
        description=settings.WEB_APP_DESCRIPTION,
        version=settings.WEB_APP_VERSION,
        lifespan=lifespan,
    )

    app.include_router(auth.router)
    app.include_router(task.router)
    app.include_router(assigned_task.router)

    return app


app = create_application()

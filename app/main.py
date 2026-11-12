from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routes import router


def create_app(db_path: str = "data/app.db") -> FastAPI:
    """Create FastAPI application and initialize SQLite database on startup."""

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        init_db(application.state.db_path)
        yield

    application = FastAPI(title="Mini Issue Tracker", lifespan=lifespan)
    application.state.db_path = db_path
    application.include_router(router)

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()

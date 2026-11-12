from fastapi import FastAPI

from app.database import init_db
from app.routes import router


def create_app(db_path: str = "data/app.db") -> FastAPI:
    """Create FastAPI application and initialize SQLite database."""
    init_db(db_path)
    application = FastAPI(title="Mini Issue Tracker")
    application.state.db_path = db_path
    application.include_router(router)

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()

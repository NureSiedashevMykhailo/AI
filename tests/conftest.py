from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture()
def db_path(tmp_path: Path) -> Path:
    """Return an isolated temporary SQLite database path."""
    return tmp_path / "test.db"


@pytest.fixture()
def client(db_path: Path) -> Generator[TestClient, None, None]:
    """Create a TestClient bound to an isolated temporary SQLite database."""
    application = create_app(str(db_path))
    with TestClient(application) as test_client:
        yield test_client

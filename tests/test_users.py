from pathlib import Path

from fastapi.testclient import TestClient

from app.database import get_connection
from app.main import create_app


def test_list_users_returns_predefined_users_ordered_by_id(client: TestClient) -> None:
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Agent A"},
        {"id": 2, "name": "Agent B"},
    ]


def test_list_users_orders_by_id_asc_regardless_of_insertion_order(
    tmp_path: Path,
) -> None:
    db_file = tmp_path / "reverse_users.db"
    conn = get_connection(db_file)
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                );
                """
            )
            conn.execute("INSERT INTO users (id, name) VALUES (?, ?)", (2, "Agent B"))
            conn.execute("INSERT INTO users (id, name) VALUES (?, ?)", (1, "Agent A"))
    finally:
        conn.close()

    application = create_app(str(db_file))
    with TestClient(application) as test_client:
        response = test_client.get("/users")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Agent A"},
        {"id": 2, "name": "Agent B"},
    ]


def test_create_app_does_not_initialize_db_before_lifespan(tmp_path: Path) -> None:
    db_file = tmp_path / "nested" / "lazy.db"

    application = create_app(str(db_file))
    assert not db_file.exists()
    assert not db_file.parent.exists()

    with TestClient(application) as test_client:
        assert db_file.exists()
        response = test_client.get("/users")
        assert response.status_code == 200

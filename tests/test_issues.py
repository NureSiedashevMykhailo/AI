import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

UTC_ISO_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def test_t01_create_issue_defaults_and_trim(client: TestClient) -> None:
    response = client.post(
        "/issues",
        json={"title": "  Fix payment gateway timeout  "},
    )

    assert response.status_code == 201
    body = response.json()
    assert isinstance(body["id"], int) and body["id"] > 0
    assert body["title"] == "Fix payment gateway timeout"
    assert body["description"] == ""
    assert body["status"] == "OPEN"
    assert body["priority"] == "medium"
    assert body["assignee_id"] is None
    assert UTC_ISO_PATTERN.match(body["created_at"])


def test_t01_create_issue_with_optional_fields_and_boundaries(
    client: TestClient,
) -> None:
    response = client.post(
        "/issues",
        json={
            "title": f"  {'a' * 120}  ",
            "description": "d" * 2000,
            "priority": "high",
            "assignee_id": 1,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "a" * 120
    assert body["description"] == "d" * 2000
    assert body["status"] == "OPEN"
    assert body["priority"] == "high"
    assert body["assignee_id"] == 1

    min_response = client.post("/issues", json={"title": " abc ", "assignee_id": 2})
    assert min_response.status_code == 201
    assert min_response.json()["title"] == "abc"
    assert min_response.json()["assignee_id"] == 2


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"title": "  ab  "},
        {"title": "     "},
        {"title": "x" * 121},
        {"title": None},
        {"title": "Valid title", "description": None},
        {"title": "Valid title", "description": "d" * 2001},
        {"title": "Valid title", "priority": "HIGH"},
        {"title": "Valid title", "priority": "urgent"},
        {"title": "Valid title", "priority": None},
        {"title": "Valid title", "assignee_id": 99},
        {"title": "Valid title", "assignee_id": 0},
        {"title": "Valid title", "assignee_id": True},
        {"title": "Valid title", "id": 10},
        {"title": "Valid title", "created_at": "2026-11-01T12:00:00Z"},
        {"title": "Valid title", "status": "OPEN"},
        {"title": "Valid title", "status": "CLOSED"},
        {"title": "Valid title", "unknown_field": "unexpected"},
    ],
)
def test_t02_create_issue_validation_returns_422_without_saving(
    client: TestClient,
    payload: dict[str, object],
) -> None:
    response = client.post("/issues", json=payload)

    assert response.status_code == 422
    body = response.json()
    assert isinstance(body.get("detail"), list)
    assert len(body["detail"]) >= 1

    list_response = client.get("/issues")
    assert list_response.status_code == 200
    assert list_response.json() == []


def test_t03_list_and_get_issue_by_id(client: TestClient) -> None:
    empty_response = client.get("/issues")
    assert empty_response.status_code == 200
    assert empty_response.json() == []

    first = client.post(
        "/issues",
        json={"title": "First issue", "priority": "low"},
    ).json()
    second = client.post(
        "/issues",
        json={"title": "Second issue", "priority": "high", "assignee_id": 2},
    ).json()

    list_response = client.get("/issues")
    assert list_response.status_code == 200
    assert list_response.json() == [first, second]

    detail_response = client.get(f"/issues/{first['id']}")
    assert detail_response.status_code == 200
    assert detail_response.json() == first


@pytest.mark.parametrize("invalid_id", ["0", "-1", "abc"])
def test_t03_get_issue_invalid_id_returns_422(
    client: TestClient,
    invalid_id: str,
) -> None:
    response = client.get(f"/issues/{invalid_id}")

    assert response.status_code == 422


def test_t03_get_nonexistent_issue_returns_404(client: TestClient) -> None:
    response = client.get("/issues/9999")

    assert response.status_code == 404
    assert isinstance(response.json().get("detail"), str)


def test_t13_sqlite_persistence_across_restarts(db_path: Path) -> None:
    first_app = create_app(str(db_path))
    with TestClient(first_app) as first_client:
        created = first_client.post(
            "/issues",
            json={
                "title": "  Persist across restart  ",
                "description": "Stored in SQLite file",
                "priority": "high",
                "assignee_id": 1,
            },
        )
        assert created.status_code == 201
        created_issue = created.json()

    restarted_app = create_app(str(db_path))
    with TestClient(restarted_app) as restarted_client:
        get_one = restarted_client.get(f"/issues/{created_issue['id']}")
        assert get_one.status_code == 200
        assert get_one.json() == created_issue

        get_all = restarted_client.get("/issues")
        assert get_all.status_code == 200
        assert get_all.json() == [created_issue]

"""Additional LR3 pytest suite for acceptance criteria gaps and repository/service branches."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import database


def test_patch_issue_atomicity_valid_priority_with_invalid_assignee(
    client: TestClient,
) -> None:
    """FR: FR-03, FR-05, FR-07.
    AC: AC-04-02, AC-04-03.
    Очікуваний результат після повторного GET: GET /issues/{id} повертає 200 OK,
    початковий priority="low" та початковий assignee_id=1 залишаються без змін.
    """
    create_resp = client.post(
        "/issues",
        json={
            "title": "Atomic patch check",
            "description": "Verify all-or-nothing validation",
            "priority": "low",
            "assignee_id": 1,
        },
    )
    assert create_resp.status_code == 201
    initial_issue = create_resp.json()
    issue_id = initial_issue["id"]

    patch_resp = client.patch(
        f"/issues/{issue_id}",
        json={"priority": "high", "assignee_id": 999},
    )
    assert patch_resp.status_code == 422
    assert isinstance(patch_resp.json().get("detail"), list)

    get_resp = client.get(f"/issues/{issue_id}")
    assert get_resp.status_code == 200
    persisted = get_resp.json()
    assert persisted["priority"] == "low"
    assert persisted["assignee_id"] == 1
    assert persisted == initial_issue


def test_create_and_get_issue_with_apostrophe_in_title(client: TestClient) -> None:
    """FR: FR-01, FR-02, FR-07.
    AC: AC-01-01, AC-03-01.
    Очікуваний результат після повторного GET: GET /issues/{id} повертає 200 OK
    та точний рядок title="O'Brien" без екранування чи спотворень.
    """
    create_resp = client.post("/issues", json={"title": "O'Brien"})
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["title"] == "O'Brien"
    issue_id = created["id"]

    get_resp = client.get(f"/issues/{issue_id}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["title"] == "O'Brien"
    assert fetched["status"] == "OPEN"
    assert fetched["priority"] == "medium"
    assert fetched["assignee_id"] is None
    assert fetched == created


@pytest.mark.parametrize("target_status", ["OPEN", "IN_PROGRESS"])
def test_closed_issue_rejects_reopen_transitions(
    client: TestClient,
    target_status: str,
) -> None:
    """FR: FR-04.
    AC: AC-05-02, AC-06-02.
    Очікуваний результат після повторного GET: GET /issues/{id} повертає 200 OK,
    а поле status залишається рівним "CLOSED".
    """
    create_resp = client.post("/issues", json={"title": "Terminal status issue"})
    assert create_resp.status_code == 201
    issue_id = create_resp.json()["id"]

    close_resp = client.patch(
        f"/issues/{issue_id}/status",
        json={"status": "CLOSED"},
    )
    assert close_resp.status_code == 200
    assert close_resp.json()["status"] == "CLOSED"

    reopen_resp = client.patch(
        f"/issues/{issue_id}/status",
        json={"status": target_status},
    )
    assert reopen_resp.status_code == 409
    assert isinstance(reopen_resp.json().get("detail"), str)

    get_resp = client.get(f"/issues/{issue_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["status"] == "CLOSED"


def test_db_update_issue_empty_updates_returns_existing_row(
    client: TestClient,
    db_path: Path,
) -> None:
    """FR: FR-03, FR-07.
    AC: AC-03-01 (Розділ 6 п. 3 — ідемпотентний порожній пакет оновлень).
    Очікуваний результат після повторного GET: GET /issues/{id} повертає 200 OK
    із незмінними початковими атрибутами заявки.
    """
    create_resp = client.post(
        "/issues",
        json={"title": "Empty repo update", "priority": "low", "assignee_id": 2},
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    issue_id = created["id"]

    repo_row = database.update_issue(db_path, issue_id, {})
    assert repo_row == created

    get_resp = client.get(f"/issues/{issue_id}")
    assert get_resp.status_code == 200
    assert get_resp.json() == created


def test_db_update_issue_unsupported_column_raises_value_error(
    client: TestClient,
    db_path: Path,
) -> None:
    """FR: FR-03, FR-07.
    AC: AC-04-02 (Розділ 6 п. 4 — захист білого списку стовпців у репозиторії).
    Очікуваний результат після повторного GET: GET /issues/{id} повертає 200 OK,
    усі поля заявки та статус "OPEN" залишаються незмінними.
    """
    create_resp = client.post(
        "/issues",
        json={"title": "Whitelist repo guard", "priority": "medium", "assignee_id": 1},
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    issue_id = created["id"]

    with pytest.raises(ValueError, match="Unsupported issue columns"):
        database.update_issue(db_path, issue_id, {"status": "CLOSED"})

    get_resp = client.get(f"/issues/{issue_id}")
    assert get_resp.status_code == 200
    assert get_resp.json() == created


def test_patch_issue_returns_404_when_row_missing_on_db_update(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """FR: FR-02, FR-03, FR-07.
    AC: AC-03-02 (Розділ 7.2 — 404 Not Found при 0 оновлених рядків у UPDATE).
    Очікуваний результат після повторного GET: GET /issues/999 повертає 404 Not Found.
    """
    real_get_issue_by_id = database.get_issue_by_id
    calls = 0

    def stale_once_get(
        path: str | Path,
        issue_id: int,
    ) -> dict[str, object] | None:
        nonlocal calls
        calls += 1
        if calls == 1 and issue_id == 999:
            return {
                "id": 999,
                "title": "Transient issue",
                "description": "",
                "status": "OPEN",
                "priority": "low",
                "assignee_id": None,
                "created_at": "2026-11-01T12:00:00Z",
            }
        return real_get_issue_by_id(path, issue_id)

    monkeypatch.setattr(database, "get_issue_by_id", stale_once_get)

    patch_resp = client.patch("/issues/999", json={"priority": "high"})
    assert patch_resp.status_code == 404
    assert isinstance(patch_resp.json().get("detail"), str)

    get_resp = client.get("/issues/999")
    assert get_resp.status_code == 404


def test_patch_status_returns_404_when_row_missing_on_db_status_update(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """FR: FR-02, FR-04, FR-07.
    AC: AC-03-02 (Розділ 7.2 — 404 Not Found при 0 оновлених рядків у зміні статусу).
    Очікуваний результат після повторного GET: GET /issues/999 повертає 404 Not Found.
    """
    real_get_issue_by_id = database.get_issue_by_id
    calls = 0

    def stale_once_get(
        path: str | Path,
        issue_id: int,
    ) -> dict[str, object] | None:
        nonlocal calls
        calls += 1
        if calls == 1 and issue_id == 999:
            return {
                "id": 999,
                "title": "Transient status issue",
                "description": "",
                "status": "OPEN",
                "priority": "medium",
                "assignee_id": None,
                "created_at": "2026-11-01T12:00:00Z",
            }
        return real_get_issue_by_id(path, issue_id)

    monkeypatch.setattr(database, "get_issue_by_id", stale_once_get)

    status_resp = client.patch(
        "/issues/999/status",
        json={"status": "IN_PROGRESS"},
    )
    assert status_resp.status_code == 404
    assert isinstance(status_resp.json().get("detail"), str)

    get_resp = client.get("/issues/999")
    assert get_resp.status_code == 404

def test_student_health_endpoint_returns_ok(client):
    """FR-08 / §2.1: GET /health повертає 200 та статус роботи сервісу."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_student_patch_issue_preserves_apostrophe_in_title(client):
    """FR-03, FR-07 / AC-04-01: PATCH /issues/{id} зберігає прямий апостроф у title після повторного GET."""
    created = client.post("/issues", json={"title": "Initial title"}).json()
    issue_id = created["id"]

    patched = client.patch(f"/issues/{issue_id}", json={"title": "O'Brien's fix"})
    assert patched.status_code == 200
    assert patched.json()["title"] == "O'Brien's fix"

    fetched = client.get(f"/issues/{issue_id}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "O'Brien's fix"
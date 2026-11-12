import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.database import get_connection
from app.main import create_app

UTC_ISO_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def _create_issue(client: TestClient, title: str = "Issue for comments") -> dict[str, object]:
    response = client.post("/issues", json={"title": title})
    assert response.status_code == 201
    return response.json()


def test_t11_add_comment_success_trims_text_and_sets_utc(client: TestClient) -> None:
    issue = _create_issue(client)
    issue_id = issue["id"]

    response = client.post(
        f"/issues/{issue_id}/comments",
        json={
            "author_id": 2,
            "text": "  Root cause identified: connection pool limit reached.  ",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert isinstance(body["id"], int) and body["id"] > 0
    assert body["issue_id"] == issue_id
    assert body["author_id"] == 2
    assert body["text"] == "Root cause identified: connection pool limit reached."
    assert UTC_ISO_PATTERN.match(body["created_at"])


def test_t11_add_comment_text_length_boundaries(client: TestClient) -> None:
    issue_id = _create_issue(client)["id"]

    min_response = client.post(
        f"/issues/{issue_id}/comments",
        json={"author_id": 1, "text": "  x  "},
    )
    assert min_response.status_code == 201
    assert min_response.json()["text"] == "x"

    max_response = client.post(
        f"/issues/{issue_id}/comments",
        json={"author_id": 2, "text": f"  {'c' * 1000}  "},
    )
    assert max_response.status_code == 201
    assert max_response.json()["text"] == "c" * 1000


def test_t11_add_comment_allowed_on_in_progress_and_closed_issue(
    client: TestClient,
) -> None:
    issue_id = _create_issue(client)["id"]

    in_progress = client.patch(
        f"/issues/{issue_id}/status",
        json={"status": "IN_PROGRESS"},
    )
    assert in_progress.status_code == 200
    c1 = client.post(
        f"/issues/{issue_id}/comments",
        json={"author_id": 1, "text": "Investigation started"},
    )
    assert c1.status_code == 201

    closed = client.patch(
        f"/issues/{issue_id}/status",
        json={"status": "CLOSED"},
    )
    assert closed.status_code == 200
    c2 = client.post(
        f"/issues/{issue_id}/comments",
        json={"author_id": 2, "text": "Post-mortem note on closed issue"},
    )
    assert c2.status_code == 201
    assert c2.json()["issue_id"] == issue_id

    comments = client.get(f"/issues/{issue_id}/comments")
    assert comments.status_code == 200
    assert [item["text"] for item in comments.json()] == [
        "Investigation started",
        "Post-mortem note on closed issue",
    ]


def test_t11_add_comment_nonexistent_issue_returns_404(client: TestClient) -> None:
    response = client.post(
        "/issues/9999/comments",
        json={"author_id": 1, "text": "Valid comment"},
    )

    assert response.status_code == 404
    assert isinstance(response.json().get("detail"), str)


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"author_id": 1},
        {"text": "Missing author"},
        {"author_id": None, "text": "Null author"},
        {"author_id": 0, "text": "Zero author"},
        {"author_id": 3, "text": "Unknown author"},
        {"author_id": 99, "text": "Unknown author"},
        {"author_id": -1, "text": "Negative author"},
        {"author_id": True, "text": "Bool author"},
        {"author_id": False, "text": "Bool author"},
        {"author_id": "invalid", "text": "String author"},
        {"author_id": 1, "text": None},
        {"author_id": 1, "text": ""},
        {"author_id": 1, "text": "     "},
        {"author_id": 1, "text": "\t\n  "},
        {"author_id": 1, "text": "x" * 1001},
        {"author_id": 1, "text": "Valid", "id": 1},
        {"author_id": 1, "text": "Valid", "issue_id": 1},
        {"author_id": 1, "text": "Valid", "created_at": "2026-11-01T12:00:00Z"},
        {"author_id": 1, "text": "Valid", "extra_field": "unexpected"},
    ],
)
def test_t11_add_comment_invalid_payload_returns_422_without_saving(
    client: TestClient,
    payload: dict[str, object],
) -> None:
    issue_id = _create_issue(client)["id"]

    response = client.post(f"/issues/{issue_id}/comments", json=payload)

    assert response.status_code == 422
    body = response.json()
    assert isinstance(body.get("detail"), list)
    assert len(body["detail"]) >= 1

    listed = client.get(f"/issues/{issue_id}/comments")
    assert listed.status_code == 200
    assert listed.json() == []


def test_t11_validation_422_precedes_404_on_missing_issue(client: TestClient) -> None:
    response = client.post(
        "/issues/9999/comments",
        json={"author_id": 99, "text": "   "},
    )

    assert response.status_code == 422
    detail = response.json().get("detail")
    assert isinstance(detail, list)
    assert len(detail) == 2


@pytest.mark.parametrize("bad_id", ["0", "-1", "abc"])
def test_t11_t12_invalid_path_id_returns_422(client: TestClient, bad_id: str) -> None:
    post_resp = client.post(
        f"/issues/{bad_id}/comments",
        json={"author_id": 1, "text": "Valid"},
    )
    get_resp = client.get(f"/issues/{bad_id}/comments")

    assert post_resp.status_code == 422
    assert get_resp.status_code == 422


def test_t12_list_comments_empty_and_nonexistent_issue(client: TestClient) -> None:
    issue_id = _create_issue(client)["id"]

    empty_resp = client.get(f"/issues/{issue_id}/comments")
    assert empty_resp.status_code == 200
    assert empty_resp.json() == []

    missing_resp = client.get("/issues/9999/comments")
    assert missing_resp.status_code == 404
    assert isinstance(missing_resp.json().get("detail"), str)


def test_t12_list_comments_sorted_chronologically_and_isolated_per_issue(
    client: TestClient,
    db_path: Path,
) -> None:
    issue_a = _create_issue(client, title="Issue A")["id"]
    issue_b = _create_issue(client, title="Issue B")["id"]

    other = client.post(
        f"/issues/{issue_b}/comments",
        json={"author_id": 2, "text": "Comment for B"},
    )
    assert other.status_code == 201

    conn = get_connection(db_path)
    try:
        with conn:
            conn.executemany(
                """
                INSERT INTO comments (issue_id, author_id, text, created_at)
                VALUES (?, ?, ?, ?)
                """,
                [
                    (issue_a, 1, "Later timestamp", "2026-11-01T12:05:00Z"),
                    (issue_a, 2, "Same time first id", "2026-11-01T12:00:00Z"),
                    (issue_a, 1, "Same time second id", "2026-11-01T12:00:00Z"),
                ],
            )
    finally:
        conn.close()

    resp_a = client.get(f"/issues/{issue_a}/comments")
    assert resp_a.status_code == 200
    comments_a = resp_a.json()
    assert [c["text"] for c in comments_a] == [
        "Same time first id",
        "Same time second id",
        "Later timestamp",
    ]
    assert all(c["issue_id"] == issue_a for c in comments_a)

    resp_b = client.get(f"/issues/{issue_b}/comments")
    assert resp_b.status_code == 200
    assert [c["text"] for c in resp_b.json()] == ["Comment for B"]


def test_t12_comments_persist_across_app_restarts(db_path: Path) -> None:
    first_app = create_app(str(db_path))
    with TestClient(first_app) as first_client:
        issue_id = _create_issue(first_client, title="Persistent comments")["id"]
        created = first_client.post(
            f"/issues/{issue_id}/comments",
            json={"author_id": 1, "text": "  Persisted note  "},
        )
        assert created.status_code == 201
        created_comment = created.json()

    restarted_app = create_app(str(db_path))
    with TestClient(restarted_app) as second_client:
        listed = second_client.get(f"/issues/{issue_id}/comments")
        assert listed.status_code == 200
        assert listed.json() == [created_comment]

import re
from copy import deepcopy
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.database import (
    get_issue_by_id,
    init_db,
    update_issue,
    update_issue_status,
)
from app.main import create_app
from app.schemas import IssuePriority, IssueRead, IssueStatus
from app.services import matches_priority, matches_status

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
        {"title": "Valid title", "assignee_id": "1"},
        {"title": "Valid title", "assignee_id": "2"},
        {"title": "Valid title", "assignee_id": True},
        {"title": "Valid title", "assignee_id": False},
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


def test_sqlite_int64_overflow_issue_id_returns_404_and_db_none(
    client: TestClient,
    db_path: Path,
) -> None:
    overflow_id = 9_223_372_036_854_775_808

    get_resp = client.get(f"/issues/{overflow_id}")
    assert get_resp.status_code == 404
    assert isinstance(get_resp.json().get("detail"), str)

    patch_resp = client.patch(f"/issues/{overflow_id}", json={"priority": "high"})
    assert patch_resp.status_code == 404
    assert isinstance(patch_resp.json().get("detail"), str)

    noop_patch_resp = client.patch(f"/issues/{overflow_id}", json={})
    assert noop_patch_resp.status_code == 404
    assert isinstance(noop_patch_resp.json().get("detail"), str)

    status_resp = client.patch(
        f"/issues/{overflow_id}/status",
        json={"status": "IN_PROGRESS"},
    )
    assert status_resp.status_code == 404
    assert isinstance(status_resp.json().get("detail"), str)

    init_db(db_path)
    assert get_issue_by_id(db_path, overflow_id) is None
    assert update_issue(db_path, overflow_id, {"priority": "high"}) is None
    assert update_issue_status(db_path, overflow_id, "IN_PROGRESS") is None


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


def _create_sample_issue(
    client: TestClient,
    *,
    title: str = "Initial issue",
    description: str = "Initial description",
    priority: str = "low",
    assignee_id: int | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "title": title,
        "description": description,
        "priority": priority,
    }
    if assignee_id is not None:
        payload["assignee_id"] = assignee_id
    response = client.post("/issues", json=payload)
    assert response.status_code == 201
    return response.json()


def test_t07_partial_patch_and_assignee_management(client: TestClient) -> None:
    created = _create_sample_issue(client, assignee_id=None)
    issue_id = created["id"]

    assign_resp = client.patch(f"/issues/{issue_id}", json={"assignee_id": 2})
    assert assign_resp.status_code == 200
    assigned = assign_resp.json()
    assert assigned["assignee_id"] == 2
    assert assigned["title"] == created["title"]
    assert assigned["description"] == created["description"]
    assert assigned["priority"] == created["priority"]
    assert assigned["status"] == "OPEN"

    status_resp = client.patch(
        f"/issues/{issue_id}/status",
        json={"status": "IN_PROGRESS"},
    )
    assert status_resp.status_code == 200

    update_resp = client.patch(
        f"/issues/{issue_id}",
        json={
            "title": "  Updated title  ",
            "priority": "high",
            "assignee_id": None,
        },
    )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["title"] == "Updated title"
    assert updated["description"] == created["description"]
    assert updated["priority"] == "high"
    assert updated["assignee_id"] is None
    assert updated["status"] == "IN_PROGRESS"
    assert updated["created_at"] == created["created_at"]

    desc_resp = client.patch(f"/issues/{issue_id}", json={"description": ""})
    assert desc_resp.status_code == 200
    assert desc_resp.json()["description"] == ""
    assert desc_resp.json()["title"] == "Updated title"


def test_t08_status_transition_matrix_and_idempotency(client: TestClient) -> None:
    issue_a = _create_sample_issue(client)["id"]
    assert client.patch(f"/issues/{issue_a}/status", json={"status": "OPEN"}).status_code == 200

    in_progress = client.patch(
        f"/issues/{issue_a}/status",
        json={"status": "IN_PROGRESS"},
    )
    assert in_progress.status_code == 200
    assert in_progress.json()["status"] == "IN_PROGRESS"

    idempotent_ip = client.patch(
        f"/issues/{issue_a}/status",
        json={"status": "IN_PROGRESS"},
    )
    assert idempotent_ip.status_code == 200
    assert idempotent_ip.json()["status"] == "IN_PROGRESS"

    back_to_open = client.patch(f"/issues/{issue_a}/status", json={"status": "OPEN"})
    assert back_to_open.status_code == 409
    assert isinstance(back_to_open.json().get("detail"), str)
    assert client.get(f"/issues/{issue_a}").json()["status"] == "IN_PROGRESS"

    closed = client.patch(f"/issues/{issue_a}/status", json={"status": "CLOSED"})
    assert closed.status_code == 200
    assert closed.json()["status"] == "CLOSED"

    idempotent_closed = client.patch(
        f"/issues/{issue_a}/status",
        json={"status": "CLOSED"},
    )
    assert idempotent_closed.status_code == 200
    assert idempotent_closed.json()["status"] == "CLOSED"

    for forbidden_target in ("OPEN", "IN_PROGRESS"):
        conflict = client.patch(
            f"/issues/{issue_a}/status",
            json={"status": forbidden_target},
        )
        assert conflict.status_code == 409
        assert isinstance(conflict.json().get("detail"), str)
        assert client.get(f"/issues/{issue_a}").json()["status"] == "CLOSED"

    issue_b = _create_sample_issue(client)["id"]
    direct_close = client.patch(f"/issues/{issue_b}/status", json={"status": "CLOSED"})
    assert direct_close.status_code == 200
    assert direct_close.json()["status"] == "CLOSED"


@pytest.mark.parametrize(
    "payload",
    [
        {"title": "New title"},
        {"description": "New description"},
        {"priority": "high"},
        {"assignee_id": 2},
        {"assignee_id": None},
        {},
    ],
)
def test_t09_patch_closed_issue_returns_409_and_allows_get(
    client: TestClient,
    payload: dict[str, object],
) -> None:
    created = _create_sample_issue(client, assignee_id=1)
    issue_id = created["id"]
    close_resp = client.patch(f"/issues/{issue_id}/status", json={"status": "CLOSED"})
    assert close_resp.status_code == 200
    closed_snapshot = close_resp.json()

    patch_resp = client.patch(f"/issues/{issue_id}", json=payload)
    assert patch_resp.status_code == 409
    assert isinstance(patch_resp.json().get("detail"), str)

    get_resp = client.get(f"/issues/{issue_id}")
    assert get_resp.status_code == 200
    assert get_resp.json() == closed_snapshot


@pytest.mark.parametrize(
    "payload",
    [
        {"title": None},
        {"description": None},
        {"priority": None},
        {"title": "  ab  "},
        {"title": "     "},
        {"title": "x" * 121},
        {"description": "d" * 2001},
        {"priority": "HIGH"},
        {"priority": "urgent"},
        {"assignee_id": 99},
        {"assignee_id": 0},
        {"assignee_id": "1"},
        {"assignee_id": "2"},
        {"assignee_id": True},
        {"assignee_id": False},
    ],
)
def test_t10_patch_issue_validation_returns_422(
    client: TestClient,
    payload: dict[str, object],
) -> None:
    created = _create_sample_issue(client, assignee_id=1)
    issue_id = created["id"]

    response = client.patch(f"/issues/{issue_id}", json=payload)
    assert response.status_code == 422
    assert isinstance(response.json().get("detail"), list)
    assert client.get(f"/issues/{issue_id}").json() == created


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"status": None},
        {"status": "open"},
        {"status": "DONE"},
        {"status": "IN_PROGRESS", "extra": "field"},
    ],
)
def test_t10_patch_status_validation_returns_422(
    client: TestClient,
    payload: dict[str, object],
) -> None:
    created = _create_sample_issue(client)
    issue_id = created["id"]

    response = client.patch(f"/issues/{issue_id}/status", json=payload)
    assert response.status_code == 422
    assert isinstance(response.json().get("detail"), list)
    assert client.get(f"/issues/{issue_id}").json()["status"] == "OPEN"


@pytest.mark.parametrize("invalid_id", ["0", "-1", "abc"])
def test_t10_patch_invalid_id_returns_422(
    client: TestClient,
    invalid_id: str,
) -> None:
    assert client.patch(f"/issues/{invalid_id}", json={"priority": "high"}).status_code == 422
    assert (
        client.patch(f"/issues/{invalid_id}/status", json={"status": "IN_PROGRESS"}).status_code
        == 422
    )


def test_t10_patch_nonexistent_issue_returns_404_after_422_check(
    client: TestClient,
) -> None:
    patch_404 = client.patch("/issues/9999", json={"priority": "high"})
    assert patch_404.status_code == 404
    assert isinstance(patch_404.json().get("detail"), str)

    status_404 = client.patch("/issues/9999/status", json={"status": "IN_PROGRESS"})
    assert status_404.status_code == 404
    assert isinstance(status_404.json().get("detail"), str)

    assert client.patch("/issues/9999", json={"priority": None}).status_code == 422
    assert client.patch("/issues/9999/status", json={"status": "INVALID"}).status_code == 422


@pytest.mark.parametrize(
    "payload",
    [
        {"title": "Valid New Title", "assignee_id": 99},
        {"priority": "high", "title": "  ab  "},
        {"title": "Valid New Title", "description": None},
        {"title": "Valid New Title", "priority": None},
        {"title": "Valid New Title", "unknown_field": "unexpected"},
        {"unknown_field": "unexpected"},
        {"id": 99},
        {"created_at": "2026-11-01T12:00:00Z"},
        {"status": "IN_PROGRESS"},
        {"title": "Valid New Title", "status": "CLOSED"},
    ],
)
def test_t14_patch_atomicity_forbidden_fields_and_status_rejection(
    client: TestClient,
    payload: dict[str, object],
) -> None:
    created = _create_sample_issue(client, assignee_id=1)
    issue_id = created["id"]

    response = client.patch(f"/issues/{issue_id}", json=payload)
    assert response.status_code == 422
    assert isinstance(response.json().get("detail"), list)

    current = client.get(f"/issues/{issue_id}")
    assert current.status_code == 200
    assert current.json() == created


def test_t14_empty_patch_is_noop_for_open_and_409_for_closed(
    client: TestClient,
) -> None:
    created = _create_sample_issue(client, assignee_id=1)
    issue_id = created["id"]

    noop_open = client.patch(f"/issues/{issue_id}", json={})
    assert noop_open.status_code == 200
    assert noop_open.json() == created

    in_progress = client.patch(
        f"/issues/{issue_id}/status",
        json={"status": "IN_PROGRESS"},
    ).json()
    noop_in_progress = client.patch(f"/issues/{issue_id}", json={})
    assert noop_in_progress.status_code == 200
    assert noop_in_progress.json() == in_progress

    client.patch(f"/issues/{issue_id}/status", json={"status": "CLOSED"})
    closed_noop = client.patch(f"/issues/{issue_id}", json={})
    assert closed_noop.status_code == 409
    assert isinstance(closed_noop.json().get("detail"), str)


def test_t04_filter_issues_by_status_priority_and_combined_and(
    client: TestClient,
) -> None:
    open_high_1 = _create_sample_issue(client, title="Open high 1", priority="high")
    open_low = _create_sample_issue(client, title="Open low", priority="low")
    in_progress_high = _create_sample_issue(
        client,
        title="In progress high",
        priority="high",
    )
    in_progress_high = client.patch(
        f"/issues/{in_progress_high['id']}/status",
        json={"status": "IN_PROGRESS"},
    ).json()
    closed_medium = _create_sample_issue(
        client,
        title="Closed medium",
        priority="medium",
    )
    closed_medium = client.patch(
        f"/issues/{closed_medium['id']}/status",
        json={"status": "CLOSED"},
    ).json()
    open_high_2 = _create_sample_issue(client, title="Open high 2", priority="high")

    all_resp = client.get("/issues")
    assert all_resp.status_code == 200
    assert all_resp.json() == [
        open_high_1,
        open_low,
        in_progress_high,
        closed_medium,
        open_high_2,
    ]

    by_status = client.get("/issues", params={"status": "OPEN"})
    assert by_status.status_code == 200
    assert by_status.json() == [open_high_1, open_low, open_high_2]

    by_status_ip = client.get("/issues", params={"status": "IN_PROGRESS"})
    assert by_status_ip.status_code == 200
    assert by_status_ip.json() == [in_progress_high]

    by_priority = client.get("/issues", params={"priority": "high"})
    assert by_priority.status_code == 200
    assert by_priority.json() == [open_high_1, in_progress_high, open_high_2]

    combined = client.get("/issues", params={"status": "OPEN", "priority": "high"})
    assert combined.status_code == 200
    assert combined.json() == [open_high_1, open_high_2]


def test_t05_filter_issues_no_matches_returns_empty_list_200(
    client: TestClient,
) -> None:
    empty_db_resp = client.get(
        "/issues",
        params={"status": "OPEN", "priority": "high"},
    )
    assert empty_db_resp.status_code == 200
    assert empty_db_resp.json() == []

    _create_sample_issue(client, title="Open high", priority="high")
    ip_issue = _create_sample_issue(client, title="In progress medium", priority="medium")
    client.patch(f"/issues/{ip_issue['id']}/status", json={"status": "IN_PROGRESS"})

    no_combined = client.get(
        "/issues",
        params={"status": "CLOSED", "priority": "low"},
    )
    assert no_combined.status_code == 200
    assert no_combined.json() == []

    no_status = client.get("/issues", params={"status": "CLOSED"})
    assert no_status.status_code == 200
    assert no_status.json() == []

    no_priority = client.get("/issues", params={"priority": "low"})
    assert no_priority.status_code == 200
    assert no_priority.json() == []


@pytest.mark.parametrize(
    "query",
    [
        "status=open",
        "status=DONE",
        "status=",
        "priority=HIGH",
        "priority=urgent",
        "priority=",
        "status=OPEN&priority=HIGH",
        "status=invalid&priority=high",
    ],
)
def test_t06_filter_issues_invalid_query_params_returns_422(
    client: TestClient,
    query: str,
) -> None:
    response = client.get(f"/issues?{query}")

    assert response.status_code == 422
    body = response.json()
    assert isinstance(body.get("detail"), list)
    assert len(body["detail"]) >= 1


def test_issue_update_openapi_schema_disallows_null_for_non_nullable_fields(
    client: TestClient,
) -> None:
    openapi_resp = client.get("/openapi.json")
    assert openapi_resp.status_code == 200

    issue_update_schema = openapi_resp.json()["components"]["schemas"]["IssueUpdate"]
    properties = issue_update_schema["properties"]
    assert issue_update_schema.get("required", []) == []

    for field_name in ("title", "description", "priority"):
        field_schema = properties[field_name]
        assert "anyOf" not in field_schema
        assert field_schema.get("type") != "null"

    assert properties["title"]["type"] == "string"
    assert properties["description"]["type"] == "string"
    assert properties["priority"]["$ref"] == "#/components/schemas/IssuePriority"
    assert properties["assignee_id"]["anyOf"] == [
        {"type": "integer"},
        {"type": "null"},
    ]


def test_matches_priority_none_returns_true() -> None:
    issue_dict = {
        "id": 1,
        "title": "Sample",
        "description": "",
        "status": "OPEN",
        "priority": "low",
        "assignee_id": None,
        "created_at": "2026-11-01T12:00:00Z",
    }
    issue_model = IssueRead(**issue_dict)

    assert matches_priority(issue_dict, None) is True
    assert matches_priority(issue_model, None) is True


@pytest.mark.parametrize("priority_value", ["high", IssuePriority.high])
def test_matches_priority_exact_match_returns_true(
    priority_value: IssuePriority | str,
) -> None:
    issue_dict = {
        "id": 2,
        "title": "High priority",
        "description": "",
        "status": "OPEN",
        "priority": "high",
        "assignee_id": 1,
        "created_at": "2026-11-01T12:00:00Z",
    }
    issue_model = IssueRead(**issue_dict)

    assert matches_priority(issue_dict, priority_value) is True
    assert matches_priority(issue_model, priority_value) is True


@pytest.mark.parametrize(
    "value",
    ["low", "high", "MEDIUM", "medium ", IssuePriority.low, IssuePriority.high],
)
def test_matches_priority_mismatch_returns_false(value: IssuePriority | str) -> None:
    issue_dict = {
        "id": 3,
        "title": "Medium priority",
        "description": "",
        "status": IssueStatus.OPEN.value,
        "priority": "medium",
        "assignee_id": None,
        "created_at": "2026-11-01T12:00:00Z",
    }
    issue_model = IssueRead(**issue_dict)

    assert matches_priority(issue_dict, value) is False
    assert matches_priority(issue_model, value) is False


def test_matches_priority_does_not_mutate_input_issue() -> None:
    issue_dict = {
        "id": 4,
        "title": "Immutable check",
        "description": "Details",
        "status": "IN_PROGRESS",
        "priority": "medium",
        "assignee_id": 2,
        "created_at": "2026-11-01T12:00:00Z",
    }
    dict_snapshot = deepcopy(issue_dict)
    issue_model = IssueRead(**issue_dict)
    model_snapshot = issue_model.model_copy(deep=True)

    assert matches_priority(issue_dict, None) is True
    assert matches_priority(issue_dict, "medium") is True
    assert matches_priority(issue_dict, "high") is False
    assert issue_dict == dict_snapshot

    assert matches_priority(issue_model, None) is True
    assert matches_priority(issue_model, IssuePriority.medium) is True
    assert matches_priority(issue_model, IssuePriority.high) is False
    assert issue_model == model_snapshot

def test_matches_status_none_returns_true():
    assert matches_status({"status": "OPEN"}, None) is True

def test_matches_status_exact_match_returns_true():
    assert matches_status({"status": "OPEN"}, "OPEN") is True

def test_matches_status_mismatch_returns_false():
    assert matches_status({"status": "OPEN"}, "CLOSED") is False

def test_matches_status_does_not_mutate_input_issue():
    issue = {"status": "OPEN", "title": "Bug"}
    matches_status(issue, "CLOSED")
    assert issue == {"status": "OPEN", "title": "Bug"}
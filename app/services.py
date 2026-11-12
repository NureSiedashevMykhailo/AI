"""Business logic services for Mini Issue Tracker."""

from datetime import datetime, timezone
from pathlib import Path

from app import database
from app.schemas import (
    CommentCreate,
    CommentRead,
    IssueCreate,
    IssuePriority,
    IssueRead,
    IssueStatus,
    IssueStatusUpdate,
    IssueUpdate,
)

ALLOWED_STATUS_TRANSITIONS: dict[IssueStatus, frozenset[IssueStatus]] = {
    IssueStatus.OPEN: frozenset({
        IssueStatus.OPEN,
        IssueStatus.IN_PROGRESS,
        IssueStatus.CLOSED,
    }),
    IssueStatus.IN_PROGRESS: frozenset({
        IssueStatus.IN_PROGRESS,
        IssueStatus.CLOSED,
    }),
    IssueStatus.CLOSED: frozenset({
        IssueStatus.CLOSED,
    }),
}


class IssueNotFoundError(Exception):
    """Raised when an issue with the requested ID does not exist."""

    def __init__(self, issue_id: int) -> None:
        self.issue_id = issue_id
        super().__init__(f"Issue {issue_id} not found")


class IssueConflictError(Exception):
    """Raised when an operation violates issue lifecycle or state rules."""


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def create_issue(db_path: str | Path, payload: IssueCreate) -> IssueRead:
    """Create a new issue with initial OPEN status and UTC timestamp."""
    row = database.insert_issue(
        db_path,
        title=payload.title,
        description=payload.description,
        status=IssueStatus.OPEN.value,
        priority=payload.priority.value,
        assignee_id=payload.assignee_id,
        created_at=_utc_now_iso(),
    )
    return IssueRead(**row)


def get_issues(
    db_path: str | Path,
    status: IssueStatus | str | None = None,
    priority: IssuePriority | str | None = None,
) -> list[IssueRead]:
    """Return issues matching optional status and priority filters (AND), ordered by created_at ASC, id ASC."""
    status_value = status.value if isinstance(status, IssueStatus) else status
    priority_value = priority.value if isinstance(priority, IssuePriority) else priority
    rows = database.list_issues(db_path)
    return [
        IssueRead(**row)
        for row in rows
        if matches_status(row, status_value) and matches_priority(row, priority_value)
    ]


def get_issue(db_path: str | Path, issue_id: int) -> IssueRead:
    """Return an issue by ID or raise IssueNotFoundError."""
    row = database.get_issue_by_id(db_path, issue_id)
    if row is None:
        raise IssueNotFoundError(issue_id)
    return IssueRead(**row)


def update_issue(
    db_path: str | Path,
    issue_id: int,
    payload: IssueUpdate,
) -> IssueRead:
    """Partially update an open issue, or reject closed/missing issues."""
    row = database.get_issue_by_id(db_path, issue_id)
    if row is None:
        raise IssueNotFoundError(issue_id)
    if row["status"] == IssueStatus.CLOSED.value:
        raise IssueConflictError("Closed issue cannot be modified")

    updates = payload.model_dump(mode="json", exclude_unset=True)
    if not updates:
        return IssueRead(**row)

    updated_row = database.update_issue(db_path, issue_id, updates)
    if updated_row is None:
        raise IssueNotFoundError(issue_id)
    return IssueRead(**updated_row)


def update_issue_status(
    db_path: str | Path,
    issue_id: int,
    payload: IssueStatusUpdate,
) -> IssueRead:
    """Transition issue status according to the 3x3 lifecycle matrix."""
    row = database.get_issue_by_id(db_path, issue_id)
    if row is None:
        raise IssueNotFoundError(issue_id)

    current_status = IssueStatus(row["status"])
    target_status = payload.status
    if target_status not in ALLOWED_STATUS_TRANSITIONS[current_status]:
        raise IssueConflictError(
            f"Invalid status transition from {current_status.value} to {target_status.value}"
        )

    if target_status == current_status:
        return IssueRead(**row)

    updated_row = database.update_issue_status(db_path, issue_id, target_status.value)
    if updated_row is None:
        raise IssueNotFoundError(issue_id)
    return IssueRead(**updated_row)


def add_comment(
    db_path: str | Path,
    issue_id: int,
    payload: CommentCreate,
) -> CommentRead:
    """Add a comment to an existing issue (including CLOSED issues)."""
    if database.get_issue_by_id(db_path, issue_id) is None:
        raise IssueNotFoundError(issue_id)

    row = database.insert_comment(
        db_path,
        issue_id=issue_id,
        author_id=payload.author_id,
        text=payload.text,
        created_at=_utc_now_iso(),
    )
    return CommentRead(**row)


def get_comments(db_path: str | Path, issue_id: int) -> list[CommentRead]:
    """Return comments for an existing issue ordered by created_at ASC, id ASC."""
    if database.get_issue_by_id(db_path, issue_id) is None:
        raise IssueNotFoundError(issue_id)

    rows = database.list_comments(db_path, issue_id)
    return [CommentRead(**row) for row in rows]

def matches_status(issue: dict, value: str | None) -> bool:
    """Return True if value is None or issue status matches value exactly."""
    if value is None:
        return True
    return issue["status"] == value


def matches_priority(issue: dict, value: str | None) -> bool:
    """Return True if value is None or issue priority matches value exactly."""
    if value is None:
        return True
    return issue["priority"] == value

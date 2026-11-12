"""Business logic services for Mini Issue Tracker."""

from datetime import datetime, timezone
from pathlib import Path

from app import database
from app.schemas import IssueCreate, IssueRead, IssueStatus


class IssueNotFoundError(Exception):
    """Raised when an issue with the requested ID does not exist."""

    def __init__(self, issue_id: int) -> None:
        self.issue_id = issue_id
        super().__init__(f"Issue {issue_id} not found")


def create_issue(db_path: str | Path, payload: IssueCreate) -> IssueRead:
    """Create a new issue with initial OPEN status and UTC timestamp."""
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    row = database.insert_issue(
        db_path,
        title=payload.title,
        description=payload.description,
        status=IssueStatus.OPEN.value,
        priority=payload.priority.value,
        assignee_id=payload.assignee_id,
        created_at=created_at,
    )
    return IssueRead(**row)


def get_issues(db_path: str | Path) -> list[IssueRead]:
    """Return all issues ordered by created_at ASC, id ASC."""
    rows = database.list_issues(db_path)
    return [IssueRead(**row) for row in rows]


def get_issue(db_path: str | Path, issue_id: int) -> IssueRead:
    """Return an issue by ID or raise IssueNotFoundError."""
    row = database.get_issue_by_id(db_path, issue_id)
    if row is None:
        raise IssueNotFoundError(issue_id)
    return IssueRead(**row)

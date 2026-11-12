"""Pydantic schemas for Mini Issue Tracker."""

from enum import Enum
from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
)

ALLOWED_USER_IDS = frozenset({1, 2})

TrimmedTitle = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=3, max_length=120),
]


def _reject_bool_assignee(value: object) -> object:
    if isinstance(value, bool):
        raise ValueError("assignee_id must be 1, 2, or null")
    return value


def _validate_allowed_assignee(value: int | None) -> int | None:
    if value is not None and value not in ALLOWED_USER_IDS:
        raise ValueError("assignee_id must be one of the predefined users: 1 or 2")
    return value


AssigneeId = Annotated[
    int | None,
    BeforeValidator(_reject_bool_assignee),
    AfterValidator(_validate_allowed_assignee),
]


class IssueStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"


class IssuePriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class IssueCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: TrimmedTitle
    description: str = Field(default="", max_length=2000)
    priority: IssuePriority = IssuePriority.medium
    assignee_id: AssigneeId = None


class IssueUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: TrimmedTitle | None = None
    description: str | None = Field(default=None, max_length=2000)
    priority: IssuePriority | None = None
    assignee_id: AssigneeId = None

    @field_validator("title", "description", "priority", mode="before")
    @classmethod
    def reject_null_for_non_nullable_fields(cls, value: object) -> object:
        if value is None:
            raise ValueError("Field cannot be null")
        return value


class IssueStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: IssueStatus


class IssueRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: IssueStatus
    priority: IssuePriority
    assignee_id: int | None
    created_at: str

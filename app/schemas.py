"""Pydantic schemas for Mini Issue Tracker."""

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

ALLOWED_USER_IDS = frozenset({1, 2})

TrimmedTitle = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=3, max_length=120),
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
    assignee_id: int | None = None

    @field_validator("assignee_id", mode="before")
    @classmethod
    def reject_non_integer_assignee(cls, value: object) -> object:
        if isinstance(value, bool):
            raise ValueError("assignee_id must be 1, 2, or null")
        return value

    @field_validator("assignee_id", mode="after")
    @classmethod
    def validate_assignee_id(cls, value: int | None) -> int | None:
        if value is not None and value not in ALLOWED_USER_IDS:
            raise ValueError("assignee_id must be one of the predefined users: 1 or 2")
        return value


class IssueRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: IssueStatus
    priority: IssuePriority
    assignee_id: int | None
    created_at: str

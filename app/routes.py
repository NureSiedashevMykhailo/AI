from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, HTTPException, Request, status
from fastapi import Path as FastAPIPath

from app import services
from app.schemas import IssueCreate, IssueRead
from app.services import IssueNotFoundError

router = APIRouter()


def _get_db_path(request: Request) -> str | Path:
    return request.app.state.db_path


@router.post("/issues", response_model=IssueRead, status_code=status.HTTP_201_CREATED)
def create_issue_endpoint(payload: IssueCreate, request: Request) -> IssueRead:
    return services.create_issue(_get_db_path(request), payload)


@router.get("/issues", response_model=list[IssueRead], status_code=status.HTTP_200_OK)
def list_issues_endpoint(request: Request) -> list[IssueRead]:
    return services.get_issues(_get_db_path(request))


@router.get("/issues/{id}", response_model=IssueRead, status_code=status.HTTP_200_OK)
def get_issue_endpoint(
    id: Annotated[int, FastAPIPath(gt=0)],
    request: Request,
) -> IssueRead:
    try:
        return services.get_issue(_get_db_path(request), id)
    except IssueNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

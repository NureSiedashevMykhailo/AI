from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, HTTPException, Request, status
from fastapi import Path as FastAPIPath

from app import services
from app.schemas import IssueCreate, IssueRead, IssueStatusUpdate, IssueUpdate
from app.services import IssueConflictError, IssueNotFoundError

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


@router.patch("/issues/{id}", response_model=IssueRead, status_code=status.HTTP_200_OK)
def update_issue_endpoint(
    id: Annotated[int, FastAPIPath(gt=0)],
    payload: IssueUpdate,
    request: Request,
) -> IssueRead:
    try:
        return services.update_issue(_get_db_path(request), id, payload)
    except IssueNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except IssueConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.patch(
    "/issues/{id}/status",
    response_model=IssueRead,
    status_code=status.HTTP_200_OK,
)
def update_issue_status_endpoint(
    id: Annotated[int, FastAPIPath(gt=0)],
    payload: IssueStatusUpdate,
    request: Request,
) -> IssueRead:
    try:
        return services.update_issue_status(_get_db_path(request), id, payload)
    except IssueNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except IssueConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

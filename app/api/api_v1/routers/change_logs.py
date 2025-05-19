from typing import Any, List

from fastapi import APIRouter, Depends, Security, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response
from app.services.change_log_service import get_change_log_by_id

router = APIRouter(prefix="/change_logs", tags=["change_logs"])


@router.get("", response_model=Response[List[schemas.ChangeLog]])
def read_change_logs(
    db: Session = Depends(deps.get_db),
        skip: int = Query(0, description="Number of records to skip (for pagination)"),
        limit: int = Query(100, description="Maximum number of records to return"),
        user_id: int = Query(0, description="Filter by user ID"),
        object_type: str = Query("", description="Filter by object type"),
        current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve all change logs.
    """
    filters = {}
    if user_id:
        filters["user_id"] = user_id
    if object_type:
        filters["object_type"] = object_type

    change_logs = crud.change_log.get_multi(db, skip=skip, limit=limit, filters=filters)

    return Response(message="", data=change_logs)


@router.post("", response_model=Response[schemas.ChangeLog])
def create_change_log(
    *,
    db: Session = Depends(deps.get_db),
    change_log_in: schemas.ChangeLogCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Create a new change log.

    ## Request Body Parameters

    - **user_id** (`integer`, required): ID of the user who made the change.
    - **object_type** (`string`, required): Type of the object that was changed.
    - **object_id** (`integer`, required): ID of the object that was changed.
    - **action** (`string`, required): Action performed on the object (e.g., create, update, delete).
    - **changes** (`list[dict]`, required): Details of the changes made, each item describing a field change with old and new values.
    - **created_at** (`datetime`, optional): Timestamp when the change was recorded. Default is None."""
    change_log = crud.change_log.create(db, obj_in=change_log_in)

    return Response(message="", data=change_log)


@router.get("/{change_log_id}", response_model=Response[schemas.ChangeLog])
def read_change_log(
    *,
    db: Session = Depends(deps.get_db),
    change_log_id: int = Path(..., description= "The ID of the change log to retrieve"),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Get a specific change log by ID.
    """
    change_log = get_change_log_by_id(db, change_log_id)
    return Response(message="", data=change_log)
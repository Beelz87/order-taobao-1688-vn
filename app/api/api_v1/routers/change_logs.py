from typing import Any, List

from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response

router = APIRouter(prefix="/change_logs", tags=["change_logs"])


@router.get("", response_model=Response[List[schemas.ChangeLog]])
def read_change_logs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    user_id: int = 0,
    object_type: str = "",
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
    """
    change_log = crud.change_log.create(db, obj_in=change_log_in)

    return Response(message="", data=change_log)


@router.get("/{change_log_id}", response_model=Response[schemas.ChangeLog])
def read_change_log(
    *,
    db: Session = Depends(deps.get_db),
    change_log_id: int,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Get a specific change log by ID.
    """
    change_log = crud.change_log.get(db, id=change_log_id)
    if not change_log:
        raise HTTPException(
            status_code=404,
            detail="Change log not found.",
        )

    return Response(message="", data=change_log)
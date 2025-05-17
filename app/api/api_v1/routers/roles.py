from typing import Any, List

from app import crud, schemas
from app.api import deps
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas.base.response import Response

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/", response_model=Response[List[schemas.Role]])
def get_roles(
    db: Session = Depends(deps.get_db), skip: int = Query(
        0,
        description="Number of records to skip for pagination",
        ge=0
    ),
    limit: int = Query(
        100,
        description="Maximum number of records to return",
        ge=1, le=1000
    ),
) -> Any:
    """
    Retrieve all available user roles.
    """
    roles = crud.role.get_multi(db, skip=skip, limit=limit)

    return Response(message="", data=roles)

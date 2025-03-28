from typing import Any, List

from app import crud, schemas
from app.api import deps
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.base.response import Response

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/", response_model=Response[List[schemas.Role]])
def get_roles(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100,
) -> Any:
    """
    Retrieve all available user roles.
    """
    roles = crud.role.get_multi(db, skip=skip, limit=limit)

    return Response(message="", data=roles)

from typing import Any, List

from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response

router = APIRouter(prefix="/stores", tags=["stores"])

@router.get("", response_model=Response[List[schemas.Store]])
def read_stores(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"], Role.USER["name"]],
    ),
) -> Any:
    """
    Retrieve all stores.
    """
    stores = crud.store.get_multi(db, skip=skip, limit=limit,)

    return Response(message="", data=stores)

@router.post("", response_model=Response[schemas.Store])
def create_store(
    *,
    db: Session = Depends(deps.get_db),
    store_in: schemas.StoreCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Create new store.
    """
    store = crud.store.create(db, obj_in=store_in)

    return Response(message="", data=store)


@router.put("/{store_id}", response_model=Response[schemas.Store])
def update_store(
    *,
    db: Session = Depends(deps.get_db),
    store_id: int,
    store_in: schemas.StoreUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    update store.
    """
    store = crud.store.get(db, id=store_id)
    if not store:
        raise HTTPException(
            status_code=404,
            detail="The store does not exist in the system.",
        )
    store = crud.store.update(db, db_obj=store, obj_in=store_in)

    return Response(message="", data=store)
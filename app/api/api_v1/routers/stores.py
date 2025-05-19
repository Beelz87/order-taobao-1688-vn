from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Security, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response
from app.services.store_service import update_store_service

router = APIRouter(prefix="/stores", tags=["stores"])

@router.get("", response_model=Response[List[schemas.Store]])
def read_stores(
    db: Session = Depends(deps.get_db),
        skip: int = Query(
            0,
            description="Number of records to skip for pagination",
            ge=0
        ),
        limit: int = Query(
            100,
            description="Maximum number of records to return",
            ge=1, le=1000
        ),
    type_store: Optional[int] = Query(None, description="Filter stores by their type."),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"], Role.USER["name"]],
    ),
) -> Any:
    """
    Retrieve all stores.
    """
    filters = {}
    if type_store is not None:
        filters["type_store"] = type_store
    stores = crud.store.get_multi(db, skip=skip, limit=limit, filters=filters)

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

    ## Request Body Parameters
    - **name** (`string`, required): Name of the store.
    - **description** (`string`, required): Description of the store.
    - **is_active** (`boolean`, required): Whether the store is active (true/false).
    - **type_store** (`integer`, required): Type of the store, represented as an integer.
    - **code** (`string`, required): Unique code identifier for the store.
    - **base_fee** (`float`, required): Base fee associated with the store.

    """
    store = crud.store.create(db, obj_in=store_in)

    return Response(message="", data=store)


@router.put("/{store_id}", response_model=Response[schemas.Store])
def update_store(
    *,
    db: Session = Depends(deps.get_db),
    store_id: int = Path(..., description="The ID of the store to retrieve."),
    store_in: schemas.StoreUpdate,
    # current_user: models.User = Security(
    #     deps.get_current_active_user,
    #     scopes=[Role.SUPER_ADMIN["name"]],
    # ),
) -> Any:
    """
    update store.

    ## Request Body Parameters
    - **name** (`string`, required): Name of the store.
    - **description** (`string`, required): Description of the store.
    - **is_active** (`boolean`, required): Whether the store is active (true/false).
    - **type_store** (`integer`, required): Type of the store, represented as an integer.
    - **code** (`string`, required): Unique code identifier for the store.
    - **base_fee** (`float`, required): Base fee associated with the store.


    """
    store = update_store_service(db, store_id, store_in)
    return Response(message="", data=store)
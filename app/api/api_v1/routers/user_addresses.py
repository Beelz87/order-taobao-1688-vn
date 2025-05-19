from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Security, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response
from app.services.user_addresses_service import update_user_address_service
from app.utils.roles import get_user_id_from_role

router = APIRouter(prefix="/user_addresses", tags=["user_addresses"])


@router.get("", response_model=Response[List[schemas.UserAddress]])
def read_user_addresses(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, description="Number of records to skip (for pagination)"),
    limit: int = Query(100, description="Maximum number of records to return"),
    user_id: Optional[int] = Query(None, description="Filter addresses by user ID (optional)"),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"], Role.USER["name"]],
    ),
) -> Any:
    """
    Retrieve all user addresses.
    """
    final_user_id = get_user_id_from_role(current_user, user_id)
    filters = {}
    if final_user_id is not None:
        filters["user_id"] = final_user_id

    user_addresses = crud.user_address.get_multi(db, skip=skip, limit=limit, filters=filters)

    return Response(message="", data=user_addresses)

@router.post("", response_model=Response[schemas.UserAddress])
def create_user_addresses(
    *,
    db: Session = Depends(deps.get_db),
    addresses_in: schemas.UserAddressCreate,
    user_id: Optional[int] = Query(None, description= "The ID of the user to retrieve"),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.USER["name"], Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Create new user address.

    ## Request Body Parameters
    - **name** (`string`, required): Name of the user or contact person for this address.
    - **phone_number** (`string`, required): Contact phone number associated with this address.
    - **address** (`string`, required): Full address details (e.g., street, city, postal code).
    - **is_active** (`boolean`, optional): Indicates whether this address is currently active. Default is True.
    """
    final_user_id = get_user_id_from_role(current_user, user_id)

    user_addresses = crud.user_address.create(db, obj_in=addresses_in, user_id=final_user_id)

    return Response(message="", data=user_addresses)

@router.put("/{user_address_id}", response_model=Response[schemas.UserAddress])
def update_user_address(
    *,
    db: Session = Depends(deps.get_db),
    user_address_id: int = Path (..., description= "The ID of the user address to retrieve"),
    address_in: schemas.UserAddressUpdate,
    user_id: Optional[int] = Query(None, description= "The ID of the user to retrieve"),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.USER["name"], Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Update a user address.

    ## Request Body Parameters
    - **name** (`string`, required): Name of the user or contact person for this address.
    - **phone_number** (`string`, required): Contact phone number associated with this address.
    - **address** (`string`, required): Full address details (e.g., street, city, postal code).
    - **is_active** (`boolean`, optional): Indicates whether this address is currently active. Default is True.

    """
    updated_address = update_user_address_service(db, user_address_id, address_in, current_user, user_id)
    return Response(message="", data=updated_address)
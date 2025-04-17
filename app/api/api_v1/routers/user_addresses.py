from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Security, HTTPException, Query
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response

router = APIRouter(prefix="/user_addresses", tags=["user_addresses"])

def get_user_id_from_role(
    current_user: models.User,
    requested_user_id: Optional[int]
) -> int:
    if current_user.user_role == Role.USER:
        return current_user.id
    elif current_user.user_role in [Role.ADMIN, Role.SUPER_ADMIN]:
        if not requested_user_id:
            raise HTTPException(status_code=400, detail="user_id is required for admins")
        return requested_user_id
    else:
        raise HTTPException(status_code=403, detail="Unauthorized role")

@router.get("", response_model=Response[List[schemas.UserAddress]])
def read_user_addresses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = Query(None),
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

@router.post("", response_model=Response[List[schemas.UserAddress]])
def create_user_addresses(
    *,
    db: Session = Depends(deps.get_db),
    addresses_in: schemas.UserAddressCreate,
    user_id: Optional[int] = Query(None),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.USER["name"], Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Create new user addresses in bulk.
    """
    final_user_id = get_user_id_from_role(current_user, user_id)

    user_addresses = crud.user_address.create(db, addresses_in=addresses_in, user_id=final_user_id)

    return Response(message="", data=user_addresses)

@router.patch("/{user_address_id}", response_model=Response[schemas.UserAddress])
def update_user_address(
    *,
    db: Session = Depends(deps.get_db),
    user_address_id: int,
    address_in: schemas.UserAddressUpdate,
    user_id: Optional[int] = Query(None),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.USER["name"], Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Update a user address.
    """
    final_user_id = get_user_id_from_role(current_user, user_id)
    user_address = crud.user_address.get(db, user_address_id)
    if not user_address:
        raise HTTPException(
            status_code=404,
            detail="The user address does not exist in the system.",
        )
    if user_address.user_id != final_user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to update this address.",
        )

    user_address = crud.user_address.update(db, db_obj=user_address, obj_in=address_in, user_id=final_user_id)

    return Response(message="", data=user_address)
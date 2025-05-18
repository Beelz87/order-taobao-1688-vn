from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response
from app.services.user_role_service import assign_user_role_service, update_user_role_service

router = APIRouter(prefix="/user-roles", tags=["user-roles"])


@router.post("", response_model=Response[schemas.UserRole])
def assign_user_role(
    *,
    db: Session = Depends(deps.get_db),
    user_role_in: schemas.UserRoleCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Assign a role to a user after creation of a user

    ## Request Body Parameters
    - **user_id** (`integer`, required): The ID of the user to retrieve.
    - **role_id** (`integer`, required): The ID of the role to assign to the user.
    """
    user_role = assign_user_role_service(db, user_role_in)
    return Response(message="", data=user_role)


@router.put("/{user_id}", response_model=Response[schemas.UserRole])
def update_user_role(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_role_in: schemas.UserRoleUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.SUPER_ADMIN["name"]
        ],
    ),
) -> Any:
    """
    Update a users role.

    ## Request Body Parameters
    - **user_id** (`integer`, required): The ID of the user to retrieve.
    """
    user_role = update_user_role_service(db, user_id, user_role_in)
    return Response(message="", data=user_role)

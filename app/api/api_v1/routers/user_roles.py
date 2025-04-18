from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response

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
    """
    user_role = crud.user_role.get_by_user_id(db, user_id=user_role_in.user_id)
    if user_role:
        raise HTTPException(
            status_code=409,
            detail="This user has already been assigned a role.",
        )
    user_role = crud.user_role.create(db, obj_in=user_role_in)

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
    """
    user_role = crud.user_role.get_by_user_id(db, user_id=user_id)
    if not user_role:
        raise HTTPException(
            status_code=404, detail="There is no role assigned to this user",
        )
    user_role = crud.user_role.update(
        db, db_obj=user_role, obj_in=user_role_in
    )

    return Response(message="", data=user_role)

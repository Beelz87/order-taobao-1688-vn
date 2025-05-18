from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas


def assign_user_role_service(
    db: Session,
    user_role_in: schemas.UserRoleCreate,
):
    existing_user_role = crud.user_role.get_by_user_id(db, user_id=user_role_in.user_id)
    if existing_user_role:
        raise HTTPException(
            status_code=409,
            detail="This user has already been assigned a role.",
        )
    user_role = crud.user_role.create(db, obj_in=user_role_in)
    return user_role

def update_user_role_service(
    db: Session,
    user_id: int,
    user_role_in: schemas.UserRoleUpdate,
):
    user_role = crud.user_role.get_by_user_id(db, user_id=user_id)
    if not user_role:
        raise HTTPException(
            status_code=404,
            detail="There is no role assigned to this user",
        )
    updated_user_role = crud.user_role.update(db, db_obj=user_role, obj_in=user_role_in)
    return updated_user_role
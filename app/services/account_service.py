from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.constants.role import Role


def create_account_service(db: Session, account_in: schemas.AccountCreate) -> schemas.Account:
    account = crud.account.get_by_name(db, name=account_in.name)
    if account:
        raise HTTPException(
            status_code=409, detail="An account with this name already exists"
        )
    new_account = crud.account.create(db, obj_in=account_in)
    return new_account


def update_account_service(
        db: Session,
        account_id: int,
        account_in: schemas.AccountUpdate,
        current_user: models.User,
) -> schemas.Account:
    # Nếu user là account admin, chỉ được update chính account của họ
    if current_user.user_role.role.name == Role.ACCOUNT_ADMIN["name"]:
        if current_user.account_id != account_id:
            raise HTTPException(
                status_code=401,
                detail="This user does not have the permissions to update this account",
            )

    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account does not exist",
        )
    updated_account = crud.account.update(db, db_obj=account, obj_in=account_in)
    return updated_account


def add_user_to_account_service(
    db: Session,
    account_id: int,
    user_id: str,
) -> models.User:
    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=404, detail="Account does not exist",
        )
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail="User does not exist",
        )
    user_in = schemas.UserUpdate(account_id=account_id)
    updated_user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return updated_user

def get_users_for_account_service(
    db: Session,
    account_id: int,
    skip: int = 0,
    limit: int = 100,
) -> List[models.User]:
    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=404, detail="Account does not exist",
        )
    users = crud.user.get_by_account_id(db, account_id=account_id, skip=skip, limit=limit)
    return users

def get_users_for_own_account_service(
    db: Session,
    current_user: models.User,
    skip: int = 0,
    limit: int = 100,
) -> List[models.User]:
    if not current_user.account_id:
        raise HTTPException(
            status_code=400,
            detail="Current user does not belong to any account."
        )
    account = crud.account.get(db, id=current_user.account_id)
    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account does not exist",
        )
    users = crud.user.get_by_account_id(db, account_id=account.id, skip=skip, limit=limit)
    return users
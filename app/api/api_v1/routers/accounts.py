from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Security
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response
from app.services.account_service import create_account_service, update_account_service, add_user_to_account_service, \
    get_users_for_account_service, get_users_for_own_account_service

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=Response[List[schemas.Account]])
def get_accounts(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve all accounts.
    """
    accounts = crud.account.get_multi(db, skip=skip, limit=limit)

    return Response(message="", data=accounts)


@router.get("/me", response_model=Response[schemas.Account])
def get_account_for_user(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve account for a logged in user.
    """
    account = crud.account.get(db, id=current_user.account_id)

    return Response(message="", data=account)


@router.post("", response_model=Response[schemas.Account])
def create_account(
    *,
    db: Session = Depends(deps.get_db),
    account_in: schemas.AccountCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create an user account
    """
    account = create_account_service(db, account_in)
    return Response(message="", data=account)


@router.put("/{account_id}", response_model=Response[schemas.Account])
def update_account(
    *,
    db: Session = Depends(deps.get_db),
    account_id: int,
    account_in: schemas.AccountUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.SUPER_ADMIN["name"],
            Role.ACCOUNT_ADMIN["name"],
        ],
    ),
) -> Any:
    """
    Update an account.
    """
    account = update_account_service(db, account_id, account_in, current_user)
    return Response(message="", data=account)


@router.post("/{account_id}/users", response_model=Response[schemas.User])
def add_user_to_account(
    *,
    db: Session = Depends(deps.get_db),
    account_id: int,
    user_id: str = Body(..., embed=True),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a user to an account.
    """
    updated_user = add_user_to_account_service(db, account_id, user_id)
    return Response(message="", data=updated_user)


@router.get("/{account_id}/users", response_model=Response[List[schemas.User]])
def retrieve_users_for_account(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    account_id: int,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve users for an account.
    """
    account_users = get_users_for_account_service(db, account_id, skip, limit)
    return Response(message="", data=account_users)


@router.get("/users/me", response_model=Response[List[schemas.Account]])
def retrieve_users_for_own_account(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.SUPER_ADMIN["name"],
            Role.ACCOUNT_ADMIN["name"],
        ],
    ),
) -> Any:
    """
    Retrieve users for own account.
    """
    account_users = get_users_for_own_account_service(db, current_user, skip, limit)
    return Response(message="", data=account_users)

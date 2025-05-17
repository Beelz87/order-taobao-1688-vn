from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, Security, Query, Path
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr

from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from app.core.config import settings
from app.schemas.base.response import Response

from sqlalchemy.orm import Session
from typing import Any, List, Optional

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=Response[List[schemas.User]], summary="Read Users")
def read_users(
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
    id: Optional[int] = Query(
        None,
        description="Filter users by ID"
    ),
    user_code: Optional[str] = Query(
        None,
        description="Filter users by user code"
    ),
    phone_number: Optional[str] = Query(
        None,
        description="Filter users by phone number"
    ),
    email: Optional[str] = Query(
        None,
        description="Filter users by email address"
    ),
    created_at_start: Optional[datetime] = Query(
        None,
        description="Filter users created on or after this date and time (format: YYYY-MM-DDTHH:MM:SS)"
    ),
    created_at_end: Optional[datetime] = Query(
        None,
        description="Filter users created on or before this date and time (format: YYYY-MM-DDTHH:MM:SS)"
    ),
    order_by: str = Query(
        "id",
        description="Field to order results by (e.g., 'id', 'email', 'created_at')"
    ),
    direction: str = Query(
        "desc",
        description="Sort direction ('asc' for ascending, 'desc' for descending)"
    ),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve all users.
    """
    filters = {}
    if id is not None:
        filters["id"] = id
    if user_code is not None:
        filters["user_code"] = user_code
    if phone_number is not None:
        filters["phone_number"] = phone_number
    if email is not None:
        filters["email"] = email
    if created_at_start is not None:
        filters["created_at_start"] = created_at_start
    if created_at_end is not None:
        filters["created_at_end"] = created_at_end

    users = crud.user.get_multi(db, skip=skip, limit=limit, filters=filters,
                                order_by=order_by, direction=direction)

    return Response(message="", data=users)


@router.post("", response_model=Response[schemas.User])
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Create new user.

    ## Request Body Parameters
    - **email** (`string`, required): Email address of the user (must be unique).
    - **is_active** (`boolean`, optional): Whether the user is active (true/false). Default is `true`.
    - **full_name** (`string`, required): Full name of the user.
    - **phone_number** (`string`, optional): Contact number.
    - **account_id** (`integer`, optional): ID of the account the user is associated with.
    - **password** (`string`, required): Raw password (will be hashed).
    - **user_code** (`string`, optional): Optional custom code for the user.
    - **is_user_code_edited** (`boolean`, optional): Set to true if the user_code was manually modified.

    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return Response(message="", data=user)


@router.put("/me", response_model=Response[schemas.User])
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    full_name: str = Body(None),
    phone_number: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.

    ## Request Body Parameters
    - **email** (`string`, optional): New email address of the user (must be unique).
    - **phone_number** (`string`, optional): New phone number of the user.
    - **full_name** (`string`, optional): New full name of the user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if phone_number is not None:
        user_in.phone_number = phone_number
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)

    return Response(message="", data=user)


@router.get("/me", response_model=Response[schemas.User])
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    if not current_user.user_role:
        role = None
    else:
        role = current_user.user_role

    user_finance = crud.user_finance.get_by_user_id(db, user_id=current_user.id)

    user_addresses = crud.user_address.get_multi(db, filters={"user_id": current_user.id})

    user_data = schemas.User(
        id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
        full_name=current_user.full_name,
        phone_number=current_user.phone_number,
        user_code=current_user.user_code,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        user_role=role,
        user_finance=user_finance,
        user_addresses=user_addresses
    )

    return Response(message="", data=user_data)


@router.post("/open", response_model=Response[schemas.User])
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(...),
    phone_number: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.

    ## Request Body Parameters
    - **password** (`string`, required): Password for the new user.
    - **email** (`string`, required): Email address of the new user (must be unique).
    - **full_name** (`string`, required): Full name of the new user.
    - **phone_number** (`string`, optional): Phone number of the new user.

    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="The user with this email already exists in the system",
        )

    default_role = crud.role.get_by_name(db, name=Role.USER["name"])
    if not default_role:
        raise HTTPException(
            status_code=404,
            detail="Default role not found",
        )

    user_in = schemas.UserCreate(
        password=password,
        email=email,
        full_name=full_name,
        phone_number=phone_number,
    )
    user = crud.user.create(db, obj_in=user_in)

    user_role_in = schemas.UserRoleCreate(
        user_id=user.id,
        role_id=default_role.id
    )
    user_role = crud.user_role.create(db, obj_in=user_role_in)

    return Response(message="", data=user)


@router.get("/{user_id}", response_model=Response[schemas.User])
def read_user_by_id(
    user_id: int = Path(..., description="The ID of the user to retrieve"),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)

    return Response(message="", data=user)


@router.put("/{user_id}", response_model=Response[schemas.User])
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int = Path(..., description="The ID of the user to retrieve" ),
    user_in: schemas.UserUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)

    return Response(message="", data=user)

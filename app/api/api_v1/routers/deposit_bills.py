from datetime import datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Security, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.deposit import DepositStatus
from app.constants.role import Role
from app.schemas import UserFinanceUpdate, UserFinanceCreate
from app.schemas.base.response import Response
from app.services.deposit_bill_service import update_deposit_bill_service

router = APIRouter(prefix="/deposit-bills", tags=["deposit-bills"])

@router.get("", response_model=Response[List[schemas.DepositBill]])
def read_deposit_bills(
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
    created_at: Optional[datetime] = Query(
        None,
        description="Filter users created on or after this date and time (format: YYYY-MM-DDTHH:MM:SS)"
    ),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"], Role.USER["name"]],
    ),
) -> Any:
    """
    Retrieve all deposit bills.
    """
    filters = {}
    if created_at is not None:
        filters["created_at"] = created_at

    if current_user.user_role.role.name == Role.USER["name"]:
        filters["user_id"] = current_user.id

    deposit_bills = crud.deposit_bill.get_multi(db, skip=skip, limit=limit, filters=filters)

    return Response(message="", data=deposit_bills)

@router.post("", response_model=Response[schemas.DepositBill])
def create_deposit_bill(
    *,
    db: Session = Depends(deps.get_db),
    deposit_bill_in: schemas.DepositBillCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Create new deposit bill.

    ## Request Body Parameters

    - **user_id** (`integer`, required): ID of the user making the deposit.
    - **user_fullname** (`string`, required): Full name of the user making the deposit.
    - **amount** (`float`, required): Deposit amount.
    - **deposit_type** (`integer`, optional): Type of deposit. Default is CASH.
    - **note** (`string`, required): Description or note related to the deposit.
    - **status** (`integer`, optional): Status of the deposit. Default is PENDING.

    """
    deposit_bill = crud.deposit_bill.create(db, obj_in=deposit_bill_in)

    return Response(message="", data=deposit_bill)

@router.patch("/{deposit_bill_id}", response_model=Response[schemas.DepositBill])
def update_deposit_bill(
    *,
    db: Session = Depends(deps.get_db),
    deposit_bill_id: int = Path(... , description= "The ID of the deposit bill to retrieve"),
    deposit_bill_in: schemas.DepositBillUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Update deposit bill.


    ## Request Body Parameters
    - **deposit_type** (`integer`, optional): Type of deposit. Default is CASH.
    - **note** (`string`, required): Description or note related to the deposit.
    - **status** (`integer`, optional): Status of the deposit. Default is PENDING.

    """
    deposit_bill = update_deposit_bill_service(
        db=db,
        deposit_bill_id=deposit_bill_id,
        deposit_bill_in=deposit_bill_in,
        current_user=current_user
    )

    return Response(message="", data=deposit_bill)
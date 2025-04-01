from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response

router = APIRouter(prefix="/deposit-bills", tags=["deposit-bills"])

@router.get("", response_model=Response[List[schemas.DepositBill]])
def read_deposit_bills(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    created_at: datetime = None,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve all deposit bills.
    """
    filters = {}
    if created_at is not None:
        filters["created_at"] = created_at

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
    """
    deposit_bill = crud.deposit_bill.create(db, obj_in=deposit_bill_in)

    return Response(message="", data=deposit_bill)

@router.patch("/{deposit_bill_id}", response_model=Response[schemas.DepositBill])
def update_deposit_bill(
    *,
    db: Session = Depends(deps.get_db),
    deposit_bill_id: int,
    deposit_bill_in: schemas.DepositBillUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Update deposit bill.
    """
    deposit_bill = crud.deposit_bill.get(db, id=deposit_bill_id)
    if not deposit_bill:
        raise HTTPException(
            status_code=404,
            detail="The deposit bill does not exist in the system.",
        )
    deposit_bill = crud.deposit_bill.update(db, db_obj=deposit_bill, obj_in=deposit_bill_in)

    return Response(message="", data=deposit_bill)
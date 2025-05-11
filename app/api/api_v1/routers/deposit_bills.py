from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.deposit import DepositStatus
from app.constants.role import Role
from app.schemas import UserFinanceUpdate, UserFinanceCreate
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

    if deposit_bill.status != DepositStatus.PENDING.value:
        raise HTTPException(
            status_code=400,
            detail="The deposit bill has already been processed.",
        )

    deposit_bill = crud.deposit_bill.update(db, db_obj=deposit_bill, obj_in=deposit_bill_in,
                                            current_user_id=current_user.id)

    if deposit_bill.status == DepositStatus.APPROVED.value:
        user_finance = crud.user_finance.get_by_user_id(db, user_id=deposit_bill.user_id)
        if not user_finance:
            crud.user_finance.create(db, obj_in=UserFinanceCreate(
                user_id=deposit_bill.user_id,
                balance=deposit_bill.amount
            ))
        else:
            new_amount = user_finance.balance + deposit_bill.amount if user_finance.balance else deposit_bill.amount
            crud.user_finance.update(db, db_obj=user_finance,
                                     obj_in=UserFinanceUpdate(
                                        balance=new_amount
                                     ),
                                    current_user_id=current_user.id)

    return Response(message="", data=deposit_bill)
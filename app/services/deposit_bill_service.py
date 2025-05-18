from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.constants.deposit import DepositStatus
from app.schemas import UserFinanceCreate, UserFinanceUpdate


def update_deposit_bill_service(
    db: Session,
    deposit_bill_id: int,
    deposit_bill_in: schemas.DepositBillUpdate,
    current_user: models.User
) -> models.DepositBill:
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

    deposit_bill = crud.deposit_bill.update(
        db,
        db_obj=deposit_bill,
        obj_in=deposit_bill_in,
        current_user_id=current_user.id,
    )

    # Nếu được duyệt, cập nhật user finance
    if deposit_bill.status == DepositStatus.APPROVED.value:
        user_finance = crud.user_finance.get_by_user_id(db, user_id=deposit_bill.user_id)
        if not user_finance:
            crud.user_finance.create(db, obj_in=UserFinanceCreate(
                user_id=deposit_bill.user_id,
                balance=deposit_bill.amount
            ))
        else:
            new_amount = (user_finance.balance or 0) + deposit_bill.amount
            crud.user_finance.update(
                db,
                db_obj=user_finance,
                obj_in=UserFinanceUpdate(balance=new_amount),
                current_user_id=current_user.id
            )

    return deposit_bill
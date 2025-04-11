from typing import Optional, Dict, Any, Union, List

from sqlalchemy.orm import Session

from app.constants.change_log import ObjectType, ActionType
from app.crud.base import CRUDBase
from app.models import ChangeLog
from app.models.deposit_bill import DepositBill
from app.schemas.deposit_bill import DepositBillCreate, DepositBillUpdate


class CRUDDepositBill(CRUDBase[DepositBill, DepositBillCreate, DepositBillUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[DepositBill]:
        return db.query(self.model).filter(DepositBill.user_id == user_id).first()

    def create(self, db: Session, *, obj_in: DepositBillCreate) -> DepositBill:
        db_obj = DepositBill(
            user_id=obj_in.user_id,
            user_fullname=obj_in.user_fullname,
            amount=obj_in.amount,
            deposit_type=obj_in.deposit_type,
            note=obj_in.note,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: DepositBill,
        obj_in: Union[DepositBillUpdate, Dict[str, Any]],
        **kwargs: Any
    ) -> DepositBill:
        current_user_id = kwargs.get("current_user_id")
        if current_user_id is None:
            raise ValueError("current_user_id is required for update operation")

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        changes = []
        for field, new_value in update_data.items():
            old_value = getattr(db_obj, field)
            if old_value != new_value:
                changes.append({
                    "field": field,
                    "old": old_value,
                    "new": new_value
                })

        updated_obj =  super().update(db, db_obj=db_obj, obj_in=update_data)

        if changes:
            change_log = ChangeLog(
                user_id=current_user_id,
                object_type=ObjectType.DEPOSIT_BILL.value,
                object_id=db_obj.id,
                action=ActionType.UPDATE.value,
                changes=changes
            )
            db.add(change_log)
            db.commit()

        return updated_obj


deposit_bill = CRUDDepositBill(DepositBill)
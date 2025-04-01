from typing import Optional, Dict, Any, Union, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
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
    ) -> DepositBill:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100, filters: Dict[str, Any] = None
    ) -> List[DepositBill]:
        query = db.query(self.model)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(self.model, key) == value)
        return query.offset(skip).limit(limit).all()


deposit_bill = CRUDDepositBill(DepositBill)
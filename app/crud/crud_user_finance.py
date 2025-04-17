from typing import Optional, Dict, Any, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user_finance import UserFinance
from app.schemas.user_finance import UserFinanceCreate, UserFinanceUpdate


class CRUDUserFinance(CRUDBase[UserFinance, UserFinanceCreate, UserFinanceUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[UserFinance]:
        return db.query(self.model).filter(UserFinance.user_id == user_id).first()

    def create(self, db: Session, *, obj_in: UserFinanceCreate, **kwargs) -> UserFinance:
        db_obj = UserFinance(
            user_id=obj_in.user_id,
            balance=obj_in.balance,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: UserFinance,
        obj_in: Union[UserFinanceUpdate, Dict[str, Any]],
        **kwargs: Any
    ) -> UserFinance:

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        updated_obj = super().update(db, db_obj=db_obj, obj_in=update_data)

        return updated_obj


user_finance = CRUDUserFinance(UserFinance)
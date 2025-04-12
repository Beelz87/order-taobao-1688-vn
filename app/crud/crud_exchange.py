from typing import Optional, Dict, Any, Union

from sqlalchemy.orm import Session

from app.constants.change_log import ObjectType, ActionType
from app.crud.base import CRUDBase
from app.models import ChangeLog
from app.models.exchanges import Exchange
from app.schemas.exchange import ExchangeCreate, ExchangeUpdate


class CRUDExchange(CRUDBase[Exchange, ExchangeCreate, ExchangeUpdate]):
    def get_active_one_by_foreign_and_local_currency(self, db: Session, *, foreign_currency: str, local_currency: str) -> Optional[Exchange]:
        return db.query(self.model).filter(Exchange.foreign_currency == foreign_currency,
                                           Exchange.local_currency == local_currency,
                                           Exchange.is_active).first()

    def create(self, db: Session, *, obj_in: ExchangeCreate) -> Exchange:
        db_obj = Exchange(
            name=obj_in.name,
            description=obj_in.description,
            foreign_currency=obj_in.foreign_currency,
            local_currency=obj_in.local_currency,
            is_active=obj_in.is_active,
            exchange_rate=obj_in.exchange_rate,
            type=obj_in.type,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Exchange,
        obj_in: Union[ExchangeUpdate, Dict[str, Any]],
        **kwargs: Any
    ) -> Exchange:
        current_user_id = kwargs.get("current_user_id")
        if current_user_id is None:
            raise ValueError("current_user_id is required for update operation")

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        changes = []
        for field, new_value in update_data.items():
            if hasattr(db_obj, field):
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
                object_type=ObjectType.EXCHANGE.value,
                object_id=db_obj.id,
                action=ActionType.UPDATE.value,
                changes=changes
            )
            db.add(change_log)
            db.commit()

        return updated_obj


exchange = CRUDExchange(Exchange)

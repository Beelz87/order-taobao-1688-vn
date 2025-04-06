from typing import Optional, Dict, Any, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
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
    ) -> Exchange:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


exchange = CRUDExchange(Exchange)

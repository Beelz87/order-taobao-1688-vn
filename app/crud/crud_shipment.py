from typing import Union, Dict, Any, List

from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Shipment
from app.schemas import ShipmentCreate, ShipmentUpdate


class CRUDShipment(CRUDBase[Shipment, ShipmentCreate, ShipmentUpdate]):
    def create(self, db: Session, *, obj_in: ShipmentCreate) -> Shipment:
        db_obj = Shipment(
            consignment_id=obj_in.consignment_id,
            shipment_status=obj_in.shipment_status,
            finance_status=obj_in.finance_status
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Shipment,
        obj_in: Union[ShipmentUpdate, Dict[str, Any]],
    ) -> Shipment:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100, filters: Dict[str, Any] = None,
                                              order_by = "id", direction = "desc"
    ) -> List[Shipment]:
        query = db.query(self.model)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(self.model, key) == value)

        try:
            if direction.lower() == "desc":
                query = query.order_by(desc(order_by))
            else:
                query = query.order_by(asc(order_by))
        except Exception as e:
            raise ValueError(f"Invalid order_by format: {order_by}") from e

        return query.offset(skip).limit(limit).all()

    def get_by_user_id(self, db: Session, *, user_id: int) -> List[Shipment]:
        return db.query(self.model).filter(Shipment.user_id == user_id).all()


shipment = CRUDShipment(Shipment)
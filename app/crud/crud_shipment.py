from typing import Union, Dict, Any, List

from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from app.constants.change_log import ObjectType, ActionType
from app.crud.base import CRUDBase
from app.models import Shipment, ChangeLog
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
        **kwargs: Any
    ) -> Shipment:
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

        updated_obj = super().update(db, db_obj=db_obj, obj_in=update_data)

        if changes:
            change_log = ChangeLog(
                user_id=current_user_id,
                object_type=ObjectType.SHIPMENT.value,
                object_id=db_obj.id,
                action=ActionType.UPDATE.value,
                changes=changes
            )
            db.add(change_log)
            db.commit()

        return updated_obj

    def get_by_user_id(self, db: Session, *, user_id: int) -> List[Shipment]:
        return db.query(self.model).filter(Shipment.user_id == user_id).all()


shipment = CRUDShipment(Shipment)
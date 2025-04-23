from typing import Union, Dict, Any, List

from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from app.constants.change_log import ObjectType, ActionType
from app.crud.base import CRUDBase
from app.models import Shipment, ChangeLog
from app.schemas import ShipmentCreate, ShipmentUpdate


class CRUDShipment(CRUDBase[Shipment, ShipmentCreate, ShipmentUpdate]):
    def create(self, db: Session, *, obj_in: ShipmentCreate, **kwargs) -> Shipment:
        db_obj = Shipment(
            consignment_id=obj_in.consignment_id,
            shipment_status=obj_in.shipment_status,
            finance_status=obj_in.finance_status,
            weight=obj_in.weight,
            height=obj_in.height,
            wide=obj_in.wide,
            length=obj_in.length,
            weight_packaged=obj_in.weight_packaged,
            height_packaged=obj_in.height_packaged,
            wide_packaged=obj_in.wide_packaged,
            length_packaged=obj_in.length_packaged,
            contains_liquid=obj_in.contains_liquid,
            is_fragile=obj_in.is_fragile,
            wooden_packaging_required=obj_in.wooden_packaging_required,
            insurance_required=obj_in.insurance_required,
            item_count_check_required=obj_in.item_count_check_required,
            contains_liquid_fee=obj_in.contains_liquid_fee,
            is_fragile_fee=obj_in.is_fragile_fee,
            wooden_packaging_required_fee=obj_in.wooden_packaging_required_fee,
            insurance_required_fee=obj_in.insurance_required_fee,
            item_count_check_required_fee=obj_in.item_count_check_required_fee,
            note=obj_in.note,
            code=obj_in.code,
            domestic_shipping_fee=obj_in.domestic_shipping_fee
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

    def remove_by_consignment_id(self, db: Session, *, consignment_id: int) -> bool:
        db.query(self.model).filter(Shipment.consignment_id == consignment_id).delete()
        db.commit()

        return True

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, filters: Dict[str, Any] = None,
                                              order_by = "id", direction = "desc"
    ) -> List[Shipment]:
        query = db.query(self.model)
        if filters:
            for key, value in filters.items():
                if key == "codes":
                    if value:
                        query = query.filter(self.model.code.in_(value))
                elif hasattr(self.model, key):  # Ensure the key exists in the model
                    query = query.filter(getattr(self.model, key) == value)
                else:
                    raise ValueError(f"Invalid filter key: {key}")

        try:
            if direction.lower() == "desc":
                query = query.order_by(desc(order_by))
            else:
                query = query.order_by(asc(order_by))
        except Exception as e:
            raise ValueError(f"Invalid order_by format: {order_by}") from e

        return query.offset(skip).limit(limit).all()


shipment = CRUDShipment(Shipment)
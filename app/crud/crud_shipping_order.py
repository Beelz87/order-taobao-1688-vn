from typing import Union, Dict, Any, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import ShippingOrder
from app.schemas.shipping_order import ShippingOrderUpdate, ShippingOrderCreate


class CRUDShippingOrder(CRUDBase[ShippingOrder, ShippingOrderCreate, ShippingOrderUpdate]):
    def create(self, db: Session, *, obj_in: ShippingOrderCreate) -> ShippingOrder:
        db_obj = ShippingOrder(
            user_id=obj_in.user_id,
            receive_store_id=obj_in.receive_store_id,
            send_store_id=obj_in.send_store_id,
            shipping_name=obj_in.shipping_name,
            shipping_address=obj_in.shipping_address,
            shipping_phone_number=obj_in.shipping_phone_number,
            shipping_status=obj_in.shipping_status,
            store_status=obj_in.store_status,
            weight=obj_in.weight,
            height=obj_in.height,
            wide=obj_in.wide,
            length=obj_in.length,
            weight_packaged=obj_in.weight_packaged,
            height_packaged=obj_in.height_packaged,
            wide_packaged=obj_in.wide_packaged,
            length_packaged=obj_in.length_packaged,
            wood_packaged_fee=obj_in.wood_packaged_fee
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ShippingOrder,
        obj_in: Union[ShippingOrderUpdate, Dict[str, Any]],
    ) -> ShippingOrder:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100,
    ) -> List[ShippingOrder]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_user_id(self, db: Session, *, user_id: int) -> List[ShippingOrder]:
        return db.query(self.model).filter(ShippingOrder.user_id == user_id).all()


shipping_order = CRUDShippingOrder(ShippingOrder)
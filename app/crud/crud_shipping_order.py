import uuid
from typing import Union, Dict, Any, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import ShippingOrder
from app.schemas.shipping_order import ShippingOrderUpdate, ShippingOrderCreate


class CRUDShippingOrder(CRUDBase[ShippingOrder, ShippingOrderCreate, ShippingOrderUpdate]):
    def create(self, db: Session, *, obj_in: ShippingOrderCreate) -> ShippingOrder:
        db_obj = ShippingOrder(
            user_id=obj_in.user_id,
            shipping_name=obj_in.shipping_name,
            shipping_phone_number=obj_in.shipping_phone_number,
            store_id=obj_in.store_id,
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
            created_at=obj_in.created_at,
            updated_at=obj_in.updated_at,
            shipping_address=obj_in.shipping_address,
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
            image_path=obj_in.image_path,
            product_category_id=obj_in.product_category_id,
            number_of_packages=obj_in.number_of_packages,
            domestic_shipping_fee=obj_in.domestic_shipping_fee,
            code=uuid.uuid4()
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
            self, db: Session, *, skip: int = 0, limit: int = 100, filters: Dict[str, Any] = None
    ) -> List[ShippingOrder]:
        query = db.query(self.model)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(self.model, key) == value)
        return query.offset(skip).limit(limit).all()

    def get_by_user_id(self, db: Session, *, user_id: int) -> List[ShippingOrder]:
        return db.query(self.model).filter(ShippingOrder.user_id == user_id).all()


shipping_order = CRUDShippingOrder(ShippingOrder)
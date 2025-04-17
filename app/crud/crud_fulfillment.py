from typing import Union, Dict, Any, List

from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Fulfillment
from app.schemas import FulfillmentCreate, FulfillmentUpdate


class CRUDFulfillment(CRUDBase[Fulfillment, FulfillmentCreate, FulfillmentUpdate]):
    def create(self, db: Session, *, obj_in: FulfillmentCreate, **kwargs) -> Fulfillment:
        db_obj = Fulfillment(
            customer_name=obj_in.customer_name,
            customer_phone_number=obj_in.customer_phone_number,
            customer_address=obj_in.customer_address,
            consignment_id=obj_in.consignment_id,
            shipment_id=obj_in.shipment_id,
            status=obj_in.status,
            shipping_type=obj_in.shipping_type
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Fulfillment,
        obj_in: Union[FulfillmentUpdate, Dict[str, Any]],
        **kwargs: Any
    ) -> Fulfillment:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_user_id(self, db: Session, *, user_id: int) -> List[Fulfillment]:
        return db.query(self.model).filter(Fulfillment.user_id == user_id).all()


fulfillment = CRUDFulfillment(Fulfillment)
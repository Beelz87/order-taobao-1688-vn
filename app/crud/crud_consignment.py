from datetime import datetime, UTC
from typing import Union, Dict, Any, List

from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from app import crud
from app.crud.base import CRUDBase
from app.models import Consignment
from app.models.consignment_foreign_shipment_code import ConsignmentForeignShipmentCode
from app.schemas.consignment import ConsignmentUpdate, ConsignmentCreate


class CRUDConsignment(CRUDBase[Consignment, ConsignmentCreate, ConsignmentUpdate]):
    def create(self, db: Session, *, obj_in: ConsignmentCreate, **kwargs) -> Consignment:
        source_store = crud.store.get(db, id=obj_in.source_store_id)
        if not source_store:
            raise ValueError(f"Store with id {obj_in.source_store_id} does not exist.")

        dest_store = crud.store.get(db, id=obj_in.dest_store_id)
        if not dest_store:
            raise ValueError(f"Store with id {obj_in.dest_store} does not exist.")

        code = f"{source_store.code}-{dest_store.code}-{obj_in.user_id}{round(datetime.now(UTC).timestamp() * 1000)}"

        user_address = crud.user_address.get(db, id=obj_in.user_address_id)
        if not user_address:
            raise ValueError(f"User address with id {obj_in.user_address_id} does not exist.")
        elif user_address.user_id != obj_in.user_id:
            raise ValueError(f"User address with id {obj_in.user_address_id} does not belong to user with id {obj_in.user_id}.")

        db_obj = Consignment(
            user_id=obj_in.user_id,
            shipping_name=user_address.name,
            shipping_phone_number=user_address.phone_number,
            shipping_address=user_address.address,
            source_store_id=obj_in.source_store_id,
            dest_store_id=obj_in.dest_store_id,
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
            image_path=obj_in.image_path,
            product_category_id=obj_in.product_category_id,
            product_name=obj_in.product_name,
            number_of_packages=obj_in.number_of_packages,
            domestic_shipping_fee=obj_in.domestic_shipping_fee,
            code=code
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        if obj_in.foreign_shipment_codes:
            for code in obj_in.foreign_shipment_codes:
                db_obj_foreign_code = ConsignmentForeignShipmentCode(
                    consignment_id=db_obj.id,
                    foreign_shipment_code=code
                )
                db.add(db_obj_foreign_code)
        db.commit()

        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Consignment,
        obj_in: Union[ConsignmentUpdate, Dict[str, Any]],
        **kwargs: Any
    ) -> Consignment:

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)


        user_address = crud.user_address.get(db, id=obj_in.user_address_id)
        if not user_address:
            raise ValueError(f"User address with id {obj_in.user_address_id} does not exist.")
        elif user_address.user_id != obj_in.user_id:
            raise ValueError(
                f"User address with id {obj_in.user_address_id} does not belong to user with id {obj_in.user_id}.")

        update_data["shipping_name"] = user_address.name
        update_data["shipping_phone_number"] = user_address.phone_number
        update_data["shipping_address"] = user_address.address

        updated_data = super().update(db, db_obj=db_obj, obj_in=update_data)

        consignment_foreign_codes = db.query(ConsignmentForeignShipmentCode).filter(
            ConsignmentForeignShipmentCode.consignment_id == db_obj.id
        ).all()
        if consignment_foreign_codes:
            for code in consignment_foreign_codes:
                db.delete(code)
            db.commit()

        if obj_in.foreign_shipment_codes:
            for code in obj_in.foreign_shipment_codes:
                db_obj_foreign_code = ConsignmentForeignShipmentCode(
                    consignment_id=db_obj.id,
                    foreign_shipment_code=code
                )
                db.add(db_obj_foreign_code)
            db.commit()

        return updated_data

    def get_by_user_id(self, db: Session, *, user_id: int) -> List[Consignment]:
        return db.query(self.model).filter(Consignment.user_id == user_id).all()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, filters: Dict[str, Any] = None,
                                              order_by = "id", direction = "desc"
    ) -> List[Consignment]:
        query = db.query(self.model)
        if filters:
            created_at_start = filters.pop("created_at_start", None)
            created_at_end = filters.pop("created_at_end", None)

            for key, value in filters.items():
                if hasattr(self.model, key):  # Ensure the key exists in the model
                    query = query.filter(getattr(self.model, key) == value)
                else:
                    raise ValueError(f"Invalid filter key: {key}")

            if created_at_start and created_at_end:
                query = query.filter(
                    self.model.created_at >= created_at_start,
                    self.model.created_at <= created_at_end
                )
            elif created_at_start and not created_at_end:
                query = query.filter(self.model.created_at >= created_at_start)
            elif not created_at_start and created_at_end:
                query = query.filter(self.model.created_at <= created_at_end)

        try:
            if direction.lower() == "desc":
                query = query.order_by(desc(order_by))
            else:
                query = query.order_by(asc(order_by))
        except Exception as e:
            raise ValueError(f"Invalid order_by format: {order_by}") from e

        return query.offset(skip).limit(limit).all()


consignment = CRUDConsignment(Consignment)

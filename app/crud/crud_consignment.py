from datetime import datetime, UTC
from typing import Union, Dict, Any, List

from sqlalchemy.orm import Session

from app import crud
from app.crud.base import CRUDBase
from app.models import Consignment
from app.models.consignment_foreign_shipment_code import ConsignmentForeignShipmentCode
from app.schemas.consignment import ConsignmentUpdate, ConsignmentCreate


class CRUDConsignment(CRUDBase[Consignment, ConsignmentCreate, ConsignmentUpdate]):
    def create(self, db: Session, *, obj_in: ConsignmentCreate) -> Consignment:
        source_store = crud.store.get(db, id=obj_in.source_store_id)
        if not source_store:
            raise ValueError(f"Store with id {obj_in.source_store} does not exist.")

        dest_store = crud.store.get(db, id=obj_in.dest_store_id)
        if not dest_store:
            raise ValueError(f"Store with id {obj_in.dest_store} does not exist.")

        product_category_code = obj_in.product_category_id
        if product_category_code > 10 and product_category_code < 100:
            product_category_code = f"0{obj_in.product_category_id}"
        elif product_category_code <10:
            product_category_code = f"00{obj_in.product_category_id}"
        code = f"{source_store.code}{dest_store.code}{product_category_code}{000}{round(datetime.now(UTC).timestamp() * 1000)}"

        db_obj = Consignment(
            user_id=obj_in.user_id,
            shipping_name=obj_in.shipping_name,
            shipping_phone_number=obj_in.shipping_phone_number,
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
    ) -> Consignment:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        updated_data = super().update(db, db_obj=db_obj, obj_in=update_data)

        consignment_foreign_codes = db.query(ConsignmentForeignShipmentCode).filter(
            ConsignmentForeignShipmentCode.consignment_id == db_obj.id
        ).all()
        if consignment_foreign_codes:
            for code in consignment_foreign_codes:
                db.delete(code)
            db.commit()

        if obj_in.foreign_shipping_code:
            for code in obj_in.foreign_shipping_code:
                db_obj_foreign_code = ConsignmentForeignShipmentCode(
                    consignment_id=db_obj.id,
                    foreign_shipment_code=code
                )
                db.add(db_obj_foreign_code)
            db.commit()

        return updated_data

    def get_by_user_id(self, db: Session, *, user_id: int) -> List[Consignment]:
        return db.query(self.model).filter(Consignment.user_id == user_id).all()


consignment = CRUDConsignment(Consignment)

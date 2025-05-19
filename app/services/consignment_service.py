import base64
import os
import uuid
from datetime import datetime, UTC

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.constants.role import Role
from app.constants.shipment import ShipmentStatus, ShipmentFinanceStatus
from app.models import User
from app.schemas import ConsignmentCreate, ShipmentCreate, ShipmentUpdate


def create_consignment_with_shipments(
    db: Session,
    consignment_in: ConsignmentCreate,
    current_user: User
):
    # Gán user_id nếu là người dùng thường
    if current_user.user_role.role.name == Role.USER["name"]:
        consignment_in.user_id = current_user.id

    # Xử lý ảnh nếu có
    if consignment_in.image_base64:
        try:
            header, base64_data = consignment_in.image_base64.split(",", 1)
        except ValueError:
            base64_data = consignment_in.image_base64

        image_data = base64.b64decode(base64_data)

        today = datetime.now(UTC)
        upload_subdir = os.path.join(
            "uploads", "consignments",
            str(today.year), f"{today.month:02}", f"{today.day:02}"
        )
        os.makedirs(upload_subdir, exist_ok=True)

        image_filename = f"{uuid.uuid4()}.jpg"
        image_path = os.path.join(upload_subdir, image_filename)

        with open(image_path, "wb") as f:
            f.write(image_data)

        consignment_in.image_path = image_path

    # Tạo consignment
    consignment = crud.consignment.create(db, obj_in=consignment_in)

    # Tạo các foreign shipments nếu có
    if consignment_in.foreign_shipment_codes:
        for code in consignment_in.foreign_shipment_codes:
            shipment_in = ShipmentCreate(
                consignment_id=consignment.id,
                shipment_status=ShipmentStatus.FOREIGN_SHIPPING.value,
                finance_status=ShipmentFinanceStatus.NOT_APPROVED.value,
                code=code
            )
            crud.shipment.create(db, obj_in=shipment_in)

    consignment.image_path = consignment_in.image_path  # Gán lại path ảnh
    return consignment

def update_consignment_with_shipments(
    db: Session,
    consignment_id: int,
    consignment_in: schemas.ConsignmentUpdate,
    current_user: models.User,
) -> models.Consignment:
    consignment = crud.consignment.get(db, id=consignment_id)
    if not consignment:
        raise HTTPException(
            status_code=404,
            detail="The consignment does not exist in the system."
        )

    if current_user.user_role == Role.USER and consignment.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action."
        )

    if consignment_in.foreign_shipment_codes:
        if not crud.shipment.remove_by_consignment_id(db, consignment_id=consignment.id):
            raise HTTPException(
                status_code=400,
                detail="Failed to remove existing foreign shipment codes."
            )

    consignment = crud.consignment.update(db, db_obj=consignment, obj_in=consignment_in)

    if consignment_in.foreign_shipment_codes:
        db_shipments = crud.shipment.get_multi(
            db, limit=1000, filters={"consignment_id": consignment.id}
        )

        for code in consignment_in.foreign_shipment_codes:
            db_shipment = next((s for s in db_shipments if s.code == code), None)
            if not db_shipment:
                shipment_in = ShipmentCreate(
                    consignment_id=consignment.id,
                    shipment_status=ShipmentStatus.FOREIGN_SHIPPING.value,
                    finance_status=ShipmentFinanceStatus.NOT_APPROVED.value,
                    code=code,
                    weight=consignment_in.weight,
                    height=consignment_in.height,
                    wide=consignment_in.wide,
                    length=consignment_in.length,
                    weight_packaged=consignment_in.weight_packaged,
                    height_packaged=consignment_in.height_packaged,
                    wide_packaged=consignment_in.wide_packaged,
                    length_packaged=consignment_in.length_packaged,
                    domestic_shipping_fee=consignment_in.domestic_shipping_fee,
                )
                crud.shipment.create(db, obj_in=shipment_in)
            else:
                shipment_in = ShipmentUpdate(
                    shipment_status=db_shipment.shipment_status,
                    finance_status=db_shipment.finance_status,
                    weight=consignment_in.weight,
                    height=consignment_in.height,
                    wide=consignment_in.wide,
                    length=consignment_in.length,
                    weight_packaged=consignment_in.weight_packaged,
                    height_packaged=consignment_in.height_packaged,
                    wide_packaged=consignment_in.wide_packaged,
                    length_packaged=consignment_in.length_packaged,
                )
                crud.shipment.update(db, db_obj=db_shipment, obj_in=shipment_in)

    return consignment
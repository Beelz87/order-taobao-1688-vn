import base64
import os
import uuid
from datetime import datetime, UTC
from typing import List, Any

from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role
from app.constants.shipment import ShipmentStatus, ShipmentFinanceStatus
from app.schemas import ShipmentCreate, ShipmentUpdate
from app.schemas.base.response import Response

router = APIRouter(prefix="/consignments", tags=["consignments"])


@router.get("", response_model=Response[List[schemas.Consignment]])
def read_consignments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    id: int = None,
    code: str = None,
    store_id: int = None,
    created_at_start: datetime = None,
    created_at_end: datetime = None,
    order_by: str = "id",
    direction: str = "desc",
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"], Role.USER["name"]],
    ),
) -> Any:
    """
    Retrieve all consignments with optional filters.
    """
    filters = {}
    if id is not None:
        filters["id"] = id
    if code is not None:
        filters["code"] = code
    if store_id is not None:
        filters["store_id"] = store_id
    if created_at_start is not None:
        filters["created_at_start"] = created_at_start
    if created_at_end is not None:
        filters["created_at_end"] = created_at_end

    if current_user.user_role.role.name == Role.USER["name"]:
       filters["user_id"] = current_user.id

    consignments = crud.consignment.get_multi(db, skip=skip, limit=limit, filters=filters,
                                                 order_by=order_by, direction=direction)

    return Response(message="", data=consignments)


@router.post("", response_model=Response[schemas.Consignment])
def create_consignment(
    *,
    db: Session = Depends(deps.get_db),
    consignment_in: schemas.ConsignmentCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"], Role.USER["name"]],
    ),
):
    """
    Create new consignment with optional image (base64).
    """
    if current_user.user_role.role.name == Role.USER["name"]:
        consignment_in.user_id = current_user.id

    if consignment_in.image_base64:
        # 1. Xử lý base64
        try:
            header, base64_data = consignment_in.image_base64.split(",", 1)
        except ValueError:
            base64_data = consignment_in.image_base64

        image_data = base64.b64decode(base64_data)

        # 2. Tạo thư mục lưu ảnh theo ngày
        today = datetime.now(UTC)
        upload_subdir = os.path.join(
            "uploads",
            "consignments",
            str(today.year),
            f"{today.month:02}",
            f"{today.day:02}"
        )
        os.makedirs(upload_subdir, exist_ok=True)

        # 3. Tạo file ảnh và lưu
        image_filename = f"{uuid.uuid4()}.jpg"
        image_path = os.path.join(upload_subdir, image_filename)

        with open(image_path, "wb") as f:
            f.write(image_data)

        # 4. Lưu thông tin vào DB
        consignment_in.image_path = image_path  # full relative path
    consignment = crud.consignment.create(db, obj_in=consignment_in)

    if consignment_in.foreign_shipment_codes:
        for code in consignment_in.foreign_shipment_codes:
            shipment_in = ShipmentCreate(consignment_id=consignment.id,
                                         shipment_status=ShipmentStatus.FOREIGN_SHIPPING.value,
                                         finance_status=ShipmentFinanceStatus.NOT_APPROVED.value,
                                         code=code
                                         )
            crud.shipment.create(db, obj_in=shipment_in)

    consignment.image_path = consignment_in.image_path
    return Response(message="", data=consignment)


@router.put("/{consignment_id}", response_model=Response[schemas.Consignment])
def update_consignment(
    *,
    db: Session = Depends(deps.get_db),
    consignment_id: int,
    consignment_in: schemas.ConsignmentUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"], Role.USER["name"]],
    ),
) -> Any:
    """
    update consignment.
    """
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
        db_shipments = crud.shipment.get_multi(db, limit=1000, filters={"consignment_id": consignment.id})
        for code in consignment_in.foreign_shipment_codes:
            db_shipment = next((s for s in db_shipments if s.code == code), None)
            if not db_shipment:
                shipment_in = ShipmentCreate(consignment_id=consignment.id,
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
                                             domestic_shipping_fee=consignment_in.domestic_shipping_fee)

                crud.shipment.create(db, obj_in=shipment_in)
            else:
                shipment_in = ShipmentUpdate(shipment_status=db_shipment.shipment_status,
                                             finance_status=db_shipment.finance_status,
                                             weight=consignment_in.weight,
                                             height=consignment_in.height,
                                             wide=consignment_in.wide,
                                             length=consignment_in.length,
                                             weight_packaged=consignment_in.weight_packaged,
                                             height_packaged=consignment_in.height_packaged,
                                             wide_packaged=consignment_in.wide_packaged,
                                             length_packaged=consignment_in.length_packaged)

                crud.shipment.update(db, db_obj=db_shipment, obj_in=shipment_in)

    return Response(message="", data=consignment)

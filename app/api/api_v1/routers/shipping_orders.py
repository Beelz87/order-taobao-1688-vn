import base64
import os
import uuid
from datetime import datetime, UTC
from typing import List, Any

from fastapi import APIRouter, Depends, Security, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role

router = APIRouter(prefix="/shipping_orders", tags=["shipping-orders"])


@router.get("", response_model=List[schemas.ShippingOrder])
def read_shipping_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"], Role.USER["name"]],
    ),
) -> Any:
    """
    Retrieve all shipping_orders.
    """

    shipping_orders = []
    if current_user.user_role == Role.ADMIN:
        shipping_orders = crud.shipping_order.get_multi(db, skip=skip, limit=limit)
    elif current_user.user_role == Role.USER:
        shipping_orders = crud.shipping_order.get_multi_by_user(
            db, user_id=current_user.id, skip=skip, limit=limit)

    return shipping_orders


@router.post("", response_model=schemas.ShippingOrder)
def create_shipping_order(
    *,
    db: Session = Depends(deps.get_db),
    shipping_order_in: schemas.ShippingOrderCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"], Role.USER["name"]],
    ),
):
    """
    Create new shipping_order with optional image (base64).
    """
    if current_user.user_role == Role.USER:
        shipping_order_in.user_id = current_user.id

    image_filename = None

    if shipping_order_in.image_base64:
        # 1. Xử lý base64
        try:
            header, base64_data = shipping_order_in.image_base64.split(",", 1)
        except ValueError:
            base64_data = shipping_order_in.image_base64

        image_data = base64.b64decode(base64_data)

        # 2. Tạo thư mục lưu ảnh theo ngày
        today = datetime.now(UTC)
        upload_subdir = os.path.join(
            "uploads",
            "shipping_orders",
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
    shipping_order_data = shipping_order_in.model_dump()
    if image_filename:
        shipping_order_data["image_path"] = image_path  # full relative path

    shipping_order = crud.shipping_order.create(db, obj_in=shipping_order_data)
    return shipping_order


@router.put("/{shipping_order_id}", response_model=schemas.ShippingOrder)
def update_shipping_order(
    *,
    db: Session = Depends(deps.get_db),
    shipping_order_id: UUID4,
    store_in: schemas.StoreUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"], Role.USER["name"]],
    ),
) -> Any:
    """
    update shipping_order.
    """
    shipping_order = crud.shipping_order.get(db, id=shipping_order_id)
    if not shipping_order:
        raise HTTPException(
            status_code=404,
            detail="The store does not exist in the system."
        )

    if shipping_order.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action."
        )

    shipping_order = crud.shipping_order.update(db, obj_in=store_in)
    return shipping_order
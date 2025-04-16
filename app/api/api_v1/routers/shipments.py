from typing import Any, List

from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.fulfillment import FulfillmentShippingType, FulfillmentStatus
from app.constants.role import Role
from app.constants.shipment import ShipmentStatus
from app.schemas.base.response import Response

router = APIRouter(prefix="/shipments", tags=["shipments"])

@router.get("", response_model=Response[List[schemas.Shipment]])
def read_shipments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    consignment_id: int = None,
    shipment_status: int = None,
    finance_status: int = None,
    foreign_shipment_code: str = None,
    order_by: str = "id",
    direction: str = "desc",
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve all shipments with optional filters.
    """
    filters = {}
    if consignment_id is not None:
        filters["consignment_id"] = consignment_id
    if shipment_status is not None:
        filters["shipment_status"] = shipment_status
    if finance_status is not None:
        filters["finance_status"] = finance_status
    if foreign_shipment_code is not None:
        filters["code"] = foreign_shipment_code

    shipments = []
    if (current_user.user_role.role.name == Role.ADMIN["name"] or
            current_user.user_role.role.name == Role.SUPER_ADMIN["name"]):
        shipments = crud.shipment.get_multi(db, skip=skip, limit=limit, filters=filters,
                                                 order_by=order_by, direction=direction)
    elif current_user.user_role.role.name == Role.USER["name"]:
        filters["user_id"] = current_user.id
        shipments = crud.shipment.get_multi(db, skip=skip, limit=limit, filters=filters,
                                                 order_by=order_by, direction=direction)

    # shipments = crud.shipment.get_multi(db, skip=skip, limit=limit, filters=filters,
    #                                           order_by=order_by, direction=direction)

    return Response(message="", data=shipments)

@router.put("/{shipment_id}", response_model=Response[schemas.Shipment])
def update_shipment(
    *,
    db: Session = Depends(deps.get_db),
    shipment_id: int,
    shipment_in: schemas.ShipmentUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    update shipment.
    """
    db_shipment = crud.shipment.get(db, id=shipment_id)
    if not db_shipment:
        raise HTTPException(
            status_code=404,
            detail="The shipment does not exist in the system."
        )

    shipment = crud.shipment.update(db, db_obj=db_shipment, obj_in=shipment_in, current_user_id=current_user.id)
    shipment.consignment = crud.consignment.get(db, id=shipment.consignment_id)

    if (shipment.shipment_status == ShipmentStatus.VN_RECEIVED.value and
            shipment_in.shipment_status == ShipmentStatus.VN_SHIPMENT_REQUESTED.value):
        fulfillment_in = schemas.FulfillmentCreate(
            consignment_id=shipment.consignment_id,
            shipment_id=shipment.id,
            status=FulfillmentStatus.WAITING.value,
            shipping_type=FulfillmentShippingType.BUS_SHIPMENT.value
        )
        crud.fulfillment.create(db, obj_in=fulfillment_in)
    # elif (shipment_in.shipment_status == ShipmentStatus.VN_SHIPMENT_REQUESTED.value and
    #       shipment_in.shipment_status == ShipmentStatus.VN_SHIPPED.value):
    #     # tru tien o day

    return Response(message="", data=shipment)
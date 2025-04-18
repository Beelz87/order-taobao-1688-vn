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

    db_consignment = crud.consignment.get(db, id=db_shipment.consignment_id)
    if not db_consignment:
        raise HTTPException(
            status_code=404,
            detail="The consignment of this shipment does not exist in the system."
        )

    if (db_shipment.shipment_status == ShipmentStatus.VN_RECEIVED.value and
            shipment_in.shipment_status == ShipmentStatus.VN_SHIPMENT_REQUESTED.value):
        store = crud.store.get(db, id=db_consignment.dest_store_id)
        if not store:
            raise HTTPException(
                status_code=404,
                detail="The store does not exist in the system."
            )
        elif store.base_fee is None or store.base_fee < 0:
            raise HTTPException(
                status_code=422,
                detail="The store's base fee is not valid."
            )

        user_finance = crud.user_finance.get_by_user_id(db, user_id=db_consignment.user_id)

        shipping_fee = (store.base_fee * db_shipment.weight + db_shipment.wooden_packaging_required_fee +
                        db_shipment.insurance_required_fee + db_shipment.domestic_shipping_fee)

        if not user_finance:
            raise HTTPException(
                status_code=404,
                detail="User finance does not exist in the system."
            )
        elif user_finance.balance < shipping_fee:
            raise HTTPException(
                status_code=400,
                detail="Not enough balance to create fulfillment."
            )

        user_address = crud.user_address.get(db, id=db_consignment.user_address_id)
        if not user_address:
            raise HTTPException(
                status_code=404,
                detail="User address does not exist in the system."
            )

        fulfillment_in = schemas.FulfillmentCreate(
            customer_name=user_address.name,
            customer_phone_number=user_address.phone_number,
            customer_address=user_address.address,
            consignment_id=db_shipment.consignment_id,
            shipment_id=shipment_id,
            status=FulfillmentStatus.WAITING.value,
            shipping_type=FulfillmentShippingType.BUS_SHIPMENT.value
        )
        crud.fulfillment.create(db, obj_in=fulfillment_in)

        new_balance = user_finance.balance - shipping_fee
        user_finance_in = schemas.UserFinanceUpdate(
            balance=new_balance
        )
        crud.user_finance.update(db, db_obj=user_finance, obj_in=user_finance_in)

    shipment = crud.shipment.update(db, db_obj=db_shipment, obj_in=shipment_in, current_user_id=current_user.id)
    shipment.consignment = crud.consignment.get(db, id=shipment.consignment_id)

    return Response(message="", data=shipment)
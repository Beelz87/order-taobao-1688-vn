from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Security, HTTPException, Query
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
        skip: int = Query(
            0,
            description="Number of records to skip for pagination.",
            ge=0
        ),
        limit: int = Query(
            100,
            description="Maximum number of records to return.",
            ge=1, le=1000
        ),
        consignment_id: Optional[int] = Query(
            None,
            description="Filter shipments by consignment ID."
        ),
        shipment_status: Optional[int] = Query(
            None,
            description="Filter shipments by shipment status."
        ),
        finance_status: Optional[int] = Query(
            None,
            description="Filter shipments by finance status."
        ),
        foreign_shipment_code: Optional[str] = Query(
            None,
            description="Filter shipments by foreign shipment code."
        ),
        order_by: str = Query(
            "id",
            description="Field to order results by ."
        ),
        direction: str = Query(
            "desc",
            description="Sort direction: 'asc' for ascending, 'desc' for descending."
        ),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"], Role.USER["name"]],
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

    Request Body Parameters
    - **shipment_status** (`integer`, required): The current status of the shipment.
    - **finance_status** (`integer`, required): The current financial status of the shipment.
    - **contains_liquid** (`boolean`, optional): Indicates whether the shipment contains liquid. Default is false.
    - **is_fragile** (`boolean`, optional): Indicates whether the shipment contains fragile items. Default is false.
    - **wooden_packaging_required** (`boolean`, optional): Indicates whether wooden packaging is required. Default is false.
    - **insurance_required** (`boolean`, optional): Indicates whether insurance is required for the shipment. Default is false.
    - **item_count_check_required** (`boolean`, optional): Indicates whether an item count check is required. Default is false.
    - **contains_liquid_fee** (`float`, optional): Fee for handling shipments containing liquid. Default is 0.0.
    - **is_fragile_fee** (`float`, optional): Fee for handling fragile items. Default is 0.0.
    - **wooden_packaging_required_fee** (`float`, optional): Fee for wooden packaging. Default is 0.0.
    - **insurance_required_fee** (`float`, optional): Fee for shipment insurance. Default is 0.0.
    - **item_count_check_required_fee** (`float`, optional): Fee for item count check service. Default is 0.0.
    - **weight** (`float`, optional): Weight of the shipment (before packaging). Default is 0.0.
    - **height** (`float`, optional): Height of the shipment (before packaging). Default is 0.0.
    - **wide** (`float`, optional): Width of the shipment (before packaging). Default is 0.0.
    - **length** (`float`, optional): Length of the shipment (before packaging). Default is 0.0.
    - **weight_packaged** (`float`, optional): Weight of the shipment (after packaging). Default is 0.0.
    - **height_packaged** (`float`, optional): Height of the shipment (after packaging). Default is 0.0.
    - **wide_packaged** (`float`, optional): Width of the shipment (after packaging). Default is 0.0.
    - **length_packaged** (`float`, optional): Length of the shipment (after packaging). Default is 0.0.
    - **domestic_shipping_fee** (`float`, optional): Fee for domestic shipping. Default is 0.0.


    """

    db_shipment = crud.shipment.get(db, id=shipment_id)
    if not db_shipment:
        raise HTTPException(
            status_code=404,
            detail="The shipment does not exist in the system."
        )

    if db_shipment.shipment_status == ShipmentStatus.FOREIGN_SHIPPING.value:
        if shipment_in.weight <= 0:
            raise HTTPException(
                status_code=422,
                detail="The weight of the shipment must be greater than 0."
            )
    elif db_shipment.shipment_status in [ShipmentStatus.VN_RECEIVED.value,
                                       ShipmentStatus.VN_SHIPMENT_REQUESTED.value,
                                       ShipmentStatus.VN_SHIPPED.value] and shipment_in.weight != db_shipment.weight:
        raise HTTPException(
            status_code=422,
            detail="The weight can not be changed in the current status."
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
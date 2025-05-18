from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.constants.fulfillment import FulfillmentStatus, FulfillmentShippingType
from app.constants.shipment import ShipmentStatus


def update_shipment_service(
    db: Session,
    shipment_id: int,
    shipment_in: schemas.ShipmentUpdate,
    current_user: models.User
) -> models.Shipment:
    db_shipment = crud.shipment.get(db, id=shipment_id)
    if not db_shipment:
        raise HTTPException(
            status_code=404,
            detail="The shipment does not exist in the system."
        )

    if db_shipment.shipment_status == ShipmentStatus.FOREIGN_SHIPPING:
        if shipment_in.weight <= 0:
            raise HTTPException(
                status_code=422,
                detail="The weight of the shipment must be greater than 0."
            )
    elif db_shipment.shipment_status in [
        ShipmentStatus.VN_RECEIVED.value,
        ShipmentStatus.VN_SHIPMENT_REQUESTED.value,
        ShipmentStatus.VN_SHIPPED.value
    ] and shipment_in.weight != db_shipment.weight:
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

    # Check fulfillment creation logic
    if (db_shipment.shipment_status == ShipmentStatus.VN_RECEIVED.value and
            shipment_in.shipment_status == ShipmentStatus.VN_SHIPMENT_REQUESTED.value):
        _create_fulfillment_if_possible(db, db_shipment, db_consignment)

    shipment = crud.shipment.update(
        db, db_obj=db_shipment, obj_in=shipment_in, current_user_id=current_user.id
    )
    shipment.consignment = crud.consignment.get(db, id=shipment.consignment_id)

    return shipment


def _create_fulfillment_if_possible(db: Session, shipment: models.Shipment, consignment: models.Consignment):
    store = crud.store.get(db, id=consignment.dest_store_id)
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

    user_finance = crud.user_finance.get_by_user_id(db, user_id=consignment.user_id)
    if not user_finance:
        raise HTTPException(
            status_code=404,
            detail="User finance does not exist in the system."
        )

    shipping_fee = (
        store.base_fee * shipment.weight +
        shipment.wooden_packaging_required_fee +
        shipment.insurance_required_fee +
        shipment.domestic_shipping_fee
    )

    if user_finance.balance < shipping_fee:
        raise HTTPException(
            status_code=400,
            detail="Not enough balance to create fulfillment."
        )

    user_address = crud.user_address.get(db, id=consignment.user_address_id)
    if not user_address:
        raise HTTPException(
            status_code=404,
            detail="User address does not exist in the system."
        )

    fulfillment_in = schemas.FulfillmentCreate(
        customer_name=user_address.name,
        customer_phone_number=user_address.phone_number,
        customer_address=user_address.address,
        consignment_id=shipment.consignment_id,
        shipment_id=shipment.id,
        status=FulfillmentStatus.WAITING.value,
        shipping_type=FulfillmentShippingType.BUS_SHIPMENT.value
    )
    crud.fulfillment.create(db, obj_in=fulfillment_in)

    # Update user finance
    new_balance = user_finance.balance - shipping_fee
    user_finance_in = schemas.UserFinanceUpdate(balance=new_balance)
    crud.user_finance.update(db, db_obj=user_finance, obj_in=user_finance_in)
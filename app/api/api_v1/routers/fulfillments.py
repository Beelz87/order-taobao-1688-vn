from typing import Any, List

from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response

router = APIRouter(prefix="/fulfillments", tags=["fulfillments"])

@router.get("", response_model=Response[List[schemas.Fulfillment]])
def read_fulfillments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    consignment_id: int = None,
    fulfillment_status: int = None,
    finance_status: int = None,
    foreign_shipping_codes: List[str] = None,
    order_by: str = "id",
    direction: str = "desc",
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve all fulfillments with optional filters.
    """
    filters = {}
    if consignment_id is not None:
        filters["consignment_id"] = consignment_id
    if fulfillment_status is not None:
        filters["fulfillment_status"] = fulfillment_status
    if finance_status is not None:
        filters["finance_status"] = finance_status
    if foreign_shipping_codes is not None:
        shipment_filters = {
            "foreign_shipping_codes": foreign_shipping_codes
        }
        shipments = crud.shipment.get_multi(db, filters=foreign_shipping_codes)
        if not shipments:
            raise HTTPException(
                status_code=404,
                detail="The shipments do not exist in the system."
            )
        filters["shipment_id"] = [shipment.id for shipment in shipments]

    fulfillments = crud.fulfillment.get_multi(db, skip=skip, limit=limit, filters=filters,
                                              order_by=order_by, direction=direction)

    return Response(message="", data=fulfillments)

@router.put("/{fulfillment_id}", response_model=Response[schemas.Fulfillment])
def update_fulfillment(
    *,
    db: Session = Depends(deps.get_db),
    fulfillment_id: int,
    fulfillment_in: schemas.FulfillmentUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Update fulfillment.
    """
    fulfillment = crud.fulfillment.get(db, id=fulfillment_id)
    if not fulfillment:
        raise HTTPException(
            status_code=404,
            detail="The fulfillment does not exist in the system."
        )

    fulfillment = crud.fulfillment.update(db, db_obj=fulfillment, obj_in=fulfillment_in)
    fulfillment.consignment = crud.consignment.get(db, id=fulfillment.consignment_id)

    return Response(message="", data=fulfillment)
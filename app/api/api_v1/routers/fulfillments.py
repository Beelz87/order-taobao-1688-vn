from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Security, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response

router = APIRouter(prefix="/fulfillments", tags=["fulfillments"])

@router.get("", response_model=Response[List[schemas.Fulfillment]])
def read_fulfillments(
        db: Session = Depends(deps.get_db),
        skip: int = Query(0, description="Number of records to skip for pagination"),
        limit: int = Query(100, description="Maximum number of records to return"),
        consignment_id: Optional[int] = Query(None, description="Filter by consignment ID"),
        fulfillment_status: Optional[int] = Query(None, description="Filter by fulfillment status"),
        finance_status: Optional[int] = Query(None, description="Filter by finance status"),
        foreign_shipping_codes: Optional[str] = Query(
            None, description="Comma-separated list of foreign shipping codes to filter by"
        ),
        order_by: str = Query("id", description="Field to sort by (e.g., id, created_at)"),
        direction: str = Query("desc", description="Sort direction: 'asc' for ascending, 'desc' for descending"),
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
        codes_list = [code.strip() for code in foreign_shipping_codes.split(",")] if foreign_shipping_codes else None
        if codes_list:
            shipment_filters = {
                "codes": foreign_shipping_codes
            }
            shipments = crud.shipment.get_multi(db, filters=shipment_filters)
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
    fulfillment_id: int = Path(..., description= "The ID of the fulfillment to retrieve"),
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
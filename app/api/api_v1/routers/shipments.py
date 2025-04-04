from typing import Any, List

from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role
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

    shipments = []
    if current_user.user_role == Role.ADMIN:
        shipments = crud.shipment.get_multi(db, skip=skip, limit=limit, filters=filters)
    elif current_user.user_role == Role.USER:
        filters["user_id"] = current_user.id
        shipments = crud.shipment.get_multi(db, skip=skip, limit=limit, filters=filters)

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
    shipment = crud.shipment.get(db, id=shipment_id)
    if not shipment:
        raise HTTPException(
            status_code=404,
            detail="The shipment does not exist in the system."
        )

    shipment = crud.shipment.update(db, obj_in=shipment_in)
    shipment.consignment = crud.consignment.get(db, id=shipment.consignment_id)

    return Response(message="", data=shipment)
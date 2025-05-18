import base64
import os
import uuid
from datetime import datetime, UTC
from typing import List, Any, Optional

from fastapi import APIRouter, Depends, Security, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response
from app.services.consignment_service import create_consignment_with_shipments, update_consignment_with_shipments

router = APIRouter(prefix="/consignments", tags=["consignments"])


@router.get("", response_model=Response[List[schemas.Consignment]])
def read_consignments(
    db: Session = Depends(deps.get_db),
        skip: int = Query(
            0,
            description="Number of records to skip for pagination",
            ge=0
        ),
        limit: int = Query(
            100,
            description="Maximum number of records to return",
            ge=1,
            le=1000
        ),
        id: Optional[int] = Query(
            None,
            description="Filter consignments by ID"
        ),
        code: Optional[str] = Query(
            None,
            description="Filter consignments by code"
        ),
        store_id: Optional[int] = Query(
            None,
            description="Filter consignments by store ID"
        ),
        created_at_start: Optional[datetime] = Query(
            None,
            description="Filter consignments created on or after this date and time (format: YYYY-MM-DDTHH:MM:SS)"
        ),
        created_at_end: Optional[datetime] = Query(
            None,
            description="Filter consignments created on or before this date and time (format: YYYY-MM-DDTHH:MM:SS)"
        ),
        order_by: str = Query(
            "id",
            description="Field to order results by (e.g., 'id', 'code', 'created_at')"
        ),
        direction: str = Query(
            "desc",
            description="Sort direction ('asc' for ascending, 'desc' for descending)"
        ),
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

    ## Request Body Parameters

    - **user_id** (`integer`, required): ID of the user who created the consignment.
    - **source_store_id** (`integer`, required): ID of the source store where the consignment originates.
    - **dest_store_id** (`integer`, required): ID of the destination store where the consignment is sent.
    - **user_address_id** (`integer`, required): ID of the user's address receiving the consignment.
    - **shipping_status** (`integer`, required): Shipping status of the consignment.
    - **store_status** (`integer`, required): Status related to the store's handling of the consignment.
    - **weight** (`float`, required): Weight of the consignment in kilograms.
    - **height** (`float`, required): Height of the consignment in centimeters.
    - **wide** (`float`, required): Width of the consignment in centimeters.
    - **length** (`float`, required): Length of the consignment in centimeters.
    - **weight_packaged** (`float`, required): Weight of the consignment after packaging (kg).
    - **height_packaged** (`float`, required): Height of the consignment after packaging (cm).
    - **wide_packaged** (`float`, required): Width of the consignment after packaging (cm).
    - **length_packaged** (`float`, required): Length of the consignment after packaging (cm).
    - **number_of_packages** (`integer`, required): Number of individual packages within the consignment.
    - **domestic_shipping_fee** (`float`, optional, default=0.0): Domestic shipping fee associated with the consignment.
    - **product_category_id** (`integer`, optional): ID of the product category.
    - **product_name** (`string`, optional): Name of the product.
    - **note** (`string`, optional): Additional notes about the consignment.
    - **foreign_shipment_codes** (`list[str]`, optional): List of foreign shipment tracking codes.
    - **image_base64** (`string`, optional): Base64 encoded image of the consignment.
    - **image_path** (`string`, optional): File path of the consignment image uploaded during creation.
    """

    consignment = create_consignment_with_shipments(db, consignment_in, current_user)
    return Response(message="", data=consignment)


@router.put("/{consignment_id}", response_model=Response[schemas.Consignment])
def update_consignment(
    *,
    db: Session = Depends(deps.get_db),
    consignment_id: int = Path(..., description= "The ID of the consignment to retrieve"),
    consignment_in: schemas.ConsignmentUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"], Role.USER["name"]],
    ),
) -> Any:
    """
    update consignment.

    ## Request Body Parameters

    - **user_id** (`integer`, required): ID of the user who created the consignment.
    - **source_store_id** (`integer`, required): ID of the source store where the consignment originates.
    - **dest_store_id** (`integer`, required): ID of the destination store where the consignment is sent.
    - **user_address_id** (`integer`, required): ID of the user's address receiving the consignment.
    - **shipping_status** (`integer`, required): Shipping status of the consignment.
    - **store_status** (`integer`, required): Status related to the store's handling of the consignment.
    - **weight** (`float`, required): Weight of the consignment in kilograms.
    - **height** (`float`, required): Height of the consignment in centimeters.
    - **wide** (`float`, required): Width of the consignment in centimeters.
    - **length** (`float`, required): Length of the consignment in centimeters.
    - **weight_packaged** (`float`, required): Weight of the consignment after packaging (kg).
    - **height_packaged** (`float`, required): Height of the consignment after packaging (cm).
    - **wide_packaged** (`float`, required): Width of the consignment after packaging (cm).
    - **length_packaged** (`float`, required): Length of the consignment after packaging (cm).
    - **number_of_packages** (`integer`, required): Number of individual packages within the consignment.
    - **domestic_shipping_fee** (`float`, optional, default=0.0): Domestic shipping fee associated with the consignment.
    - **product_category_id** (`integer`, optional): ID of the product category.
    - **product_name** (`string`, optional): Name of the product.
    - **note** (`string`, optional): Additional notes about the consignment.
    - **foreign_shipment_codes** (`list[str]`, optional): List of foreign shipment tracking codes.
    - **image_base64** (`string`, optional): Base64 encoded image of the consignment.

    """
    consignment = update_consignment_with_shipments(db, consignment_id, consignment_in, current_user)

    return Response(message="", data=consignment)

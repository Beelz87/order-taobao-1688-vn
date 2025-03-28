from typing import Any, List

from fastapi import APIRouter, Depends, Security, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response

router = APIRouter(prefix="/product-categories", tags=["product-categories"])

@router.get("", response_model=Response[List[schemas.ProductCategory]])
def read_product_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"], Role.USER["name"]],
    ),
) -> Any:
    """
    Retrieve all product categories.
    """
    product_categories = crud.product_category.get_multi(db, skip=skip, limit=limit)

    return Response(message="", data=product_categories)

@router.post("", response_model=Response[schemas.ProductCategory])
def create_product_category(
    *,
    db: Session = Depends(deps.get_db),
    product_category_in: schemas.ProductCategoryCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Create new product category.
    """
    product_category = crud.product_category.create(db, obj_in=product_category_in)

    return Response(message="", data=product_category)

@router.put("/{product_category_id}", response_model=Response[schemas.ProductCategory])
def update_product_category(
    *,
    db: Session = Depends(deps.get_db),
    product_category_id: UUID4,
    product_category_in: schemas.ProductCategoryUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Update product category.
    """
    product_category = crud.product_category.get(db, id=product_category_id)
    if not product_category:
        raise HTTPException(
            status_code=404,
            detail="The product category does not exist in the system.",
        )
    product_category = crud.product_category.update(db, db_obj=product_category, obj_in=product_category_in)

    return Response(message="", data=product_category)
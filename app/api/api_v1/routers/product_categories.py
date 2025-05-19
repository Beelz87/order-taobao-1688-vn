from typing import Any, List

from fastapi import APIRouter, Depends, Security, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response
from app.services.product_category_service import update_product_category_service

router = APIRouter(prefix="/product-categories", tags=["product-categories"])

@router.get("", response_model=Response[List[schemas.ProductCategory]])
def read_product_categories(
    db: Session = Depends(deps.get_db),
        skip: int = Query(
            0,
            description="Number of records to skip for pagination",
            ge=0
        ),
        limit: int = Query(
            100,
            description="Maximum number of records to return",
            ge=1, le=1000
        ),
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

    ## Request Body Parameters
    - **name** (`string`, optional): Name of the product category.
    - **description** (`string`, optional): Description or details about the category.
    - **category_parent_id** (`integer`, optional): ID of the parent category (if this is a subcategory).
    - **level** (`integer`, optional): Hierarchical level of the category .
    - **is_active** (`boolean`, optional): Whether the category is currently active.
    """
    product_category = crud.product_category.create(db, obj_in=product_category_in)

    return Response(message="", data=product_category)

@router.put("/{product_category_id}", response_model=Response[schemas.ProductCategory])
def update_product_category(
    *,
    db: Session = Depends(deps.get_db),
    product_category_id: int = Path(..., description= "The ID of the product category to retrieve"),
    product_category_in: schemas.ProductCategoryUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Update product category.

    ## Request Body Parameters
    - **name** (`string`, optional): Name of the product category.
    - **description** (`string`, optional): Description or details about the category.
    - **category_parent_id** (`integer`, optional): ID of the parent category (if this is a subcategory).
    - **level** (`integer`, optional): Hierarchical level of the category .
    - **is_active** (`boolean`, optional): Whether the category is currently active.
    """
    product_category = update_product_category_service(db, product_category_id, product_category_in)

    return Response(message="", data=product_category)
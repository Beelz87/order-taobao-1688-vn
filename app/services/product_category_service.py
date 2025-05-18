from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, crud


def update_product_category_service(
    db: Session,
    product_category_id: int,
    product_category_in: schemas.ProductCategoryUpdate,
) -> models.ProductCategory:
    product_category = crud.product_category.get(db, id=product_category_id)
    if not product_category:
        raise HTTPException(
            status_code=404,
            detail="The product category does not exist in the system.",
        )
    updated_category = crud.product_category.update(
        db, db_obj=product_category, obj_in=product_category_in
    )
    return updated_category
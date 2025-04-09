from typing import List, Union, Dict, Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import ProductCategory
from app.schemas.product_category import ProductCategoryCreate, ProductCategoryUpdate


class CRUDProductCategory(CRUDBase[ProductCategory, ProductCategoryCreate, ProductCategoryUpdate]):
    def create(self, db: Session, *, obj_in: ProductCategoryCreate) -> ProductCategory:
        db_obj = ProductCategory(
            name=obj_in.name,
            description=obj_in.description,
            category_parent_id=obj_in.category_parent_id,
            level=obj_in.level,
            is_active=obj_in.is_active,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ProductCategory,
        obj_in: Union[ProductCategoryUpdate, Dict[str, Any]],
    ) -> ProductCategory:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


product_category = CRUDProductCategory(ProductCategory)
from typing import Optional

from pydantic import UUID4, BaseModel

class ProductCategoryBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    category_parent_id: Optional[UUID4]
    level: Optional[int]
    is_active: Optional[bool]


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryUpdate(ProductCategoryBase):
    pass


class ProductCategoryInDBBase(ProductCategoryBase):
    id: UUID4

    class Config:
        from_attributes = True


class ProductCategory(ProductCategoryInDBBase):
    pass


class ProductCategoryInDB(ProductCategoryInDBBase):
        pass
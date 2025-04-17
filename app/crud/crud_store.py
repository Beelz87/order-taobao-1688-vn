from typing import List, Union, Dict, Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Store
from app.schemas.store import StoreCreate, StoreUpdate


class CRUDStore(CRUDBase[Store, StoreCreate, StoreUpdate]):
    def create(self, db: Session, *, obj_in: StoreCreate, **kwargs) -> Store:
        db_obj = Store(
            name=obj_in.name,
            description=obj_in.description,
            is_active=obj_in.is_active,
            type_store=obj_in.type_store,
            code=obj_in.code,
            base_fee=obj_in.base_fee
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Store,
        obj_in: Union[StoreUpdate, Dict[str, Any]],
        **kwargs: Any
    ) -> Store:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


store = CRUDStore(Store)
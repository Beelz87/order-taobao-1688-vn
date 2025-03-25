from typing import List, Union, Dict, Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Store
from app.schemas.store import StoreCreate, StoreUpdate


class CRUDStore(CRUDBase[Store, StoreCreate, StoreUpdate]):
    def create(self, db: Session, *, obj_in: StoreCreate) -> Store:
        db_obj = Store(
            name=obj_in.name,
            description=obj_in.description,
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
        db_obj: Store,
        obj_in: Union[StoreUpdate, Dict[str, Any]],
    ) -> Store:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100,
    ) -> List[Store]:
        return db.query(self.model).offset(skip).limit(limit).all()


store = CRUDStore(Store)
from typing import Dict, Any, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.change_log import ChangeLog
from app.schemas.change_log import ChangeLogCreate


class CRUDChangeLog(CRUDBase[ChangeLog, ChangeLogCreate, None]):
    def create(self, db: Session, *, obj_in: ChangeLogCreate) -> ChangeLog:
        db_obj = ChangeLog(
            user_id=obj_in.user_id,
            object_type=obj_in.object_type,
            object_id=obj_in.object_id,
            action=obj_in.action,
            changes=obj_in.changes,
            created_at=obj_in.created_at,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


change_log = CRUDChangeLog(ChangeLog)
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud


def get_change_log_by_id(db: Session, change_log_id: int):
    change_log = crud.change_log.get(db, id=change_log_id)
    if not change_log:
        raise HTTPException(
            status_code=404,
            detail="Change log not found.",
        )
    return change_log
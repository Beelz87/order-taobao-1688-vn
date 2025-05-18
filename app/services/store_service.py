from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, crud


def update_store_service(
    db: Session,
    store_id: int,
    store_in: schemas.StoreUpdate,
) -> models.Store:
    store = crud.store.get(db, id=store_id)
    if not store:
        raise HTTPException(
            status_code=404,
            detail="The store does not exist in the system.",
        )
    updated_store = crud.store.update(db, db_obj=store, obj_in=store_in)
    return updated_store
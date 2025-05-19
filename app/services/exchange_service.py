from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.schemas import ExchangeUpdate


def create_exchange_service(db: Session, exchange_in: schemas.ExchangeCreate):
    existing = crud.exchange.get_active_one_by_foreign_and_local_currency(
        db,
        foreign_currency=exchange_in.foreign_currency,
        local_currency=exchange_in.local_currency,
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="The pair of exchange already exists in the system.",
        )

    return crud.exchange.create(db, obj_in=exchange_in)

def update_exchange_service(
    db: Session,
    exchange_id: int,
    exchange_in: schemas.ExchangeUpdate,
    # current_user_id: int
) -> models.Exchange:
    exchange = crud.exchange.get(db, exchange_id)
    if not exchange:
        raise HTTPException(
            status_code=404,
            detail="The pair of exchange does not exist in the system.",
        )

    updated_exchange = crud.exchange.update(
        db, db_obj=exchange, obj_in=exchange_in, current_user_id=None
    )
    return updated_exchange
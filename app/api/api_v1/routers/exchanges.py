from typing import Any, List

from fastapi import APIRouter, Depends, Security, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.constants.role import Role
from app.schemas.base.response import Response

router = APIRouter(prefix="/exchanges", tags=["exchanges"])

@router.get("", response_model=Response[List[schemas.Exchange]])
def read_exchanges(
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
    Retrieve all exchanges.
    """
    exchanges = crud.exchange.get_multi(db, skip=skip, limit=limit,)

    return Response(message="", data=exchanges)

@router.post("", response_model=Response[schemas.Exchange])
def create_exchange(
    *,
    db: Session = Depends(deps.get_db),
    exchange_in: schemas.ExchangeCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Create new exchange.

    ## Request Body Parameters
    - **name** (`string`, required): The name of the exchange pair.
    - **description** (`string`, required): Description of the exchange pair.
    - **foreign_currency** (`string`, required): The foreign currency code
    - **local_currency** (`string`, required): The local currency code
    - **is_active** (`boolean`, required): Whether the exchange is currently active.
    - **exchange_rate** (`float`, required): The exchange rate from foreign to local currency.
    - **type** (`integer`, required): The exchange type identifier

    """
    exchange = crud.exchange.get_active_one_by_foreign_and_local_currency(db, foreign_currency=exchange_in.foreign_currency,
                                                                      local_currency=exchange_in.local_currency)
    if exchange:
        raise HTTPException(
            status_code=409,
            detail="The pair of exchange already exists in the system.",
        )
    exchange = crud.exchange.create(db, obj_in=exchange_in)

    return Response(message="", data=exchange)


@router.patch("/{exchange_id}", response_model=Response[schemas.Exchange])
def update_exchange(
    *,
    db: Session = Depends(deps.get_db),
    exchange_id: int = Path(..., description="The ID of the exchange to update."),
    exchange_in: schemas.ExchangeUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Update exchange.

     ## Request Body Parameters
    - **description** (`string`, optional): Description of the exchange pair.
    - **is_active** (`boolean`, optional): Whether the exchange is currently active.
    - **exchange_rate** (`float`, optional): The exchange rate value.

    """
    exchange = crud.exchange.get(db, exchange_id)
    if not exchange:
        raise HTTPException(
            status_code=404,
            detail="The pair of exchange does not exist in the system.",
        )
    exchange = crud.exchange.update(db, db_obj=exchange, obj_in=exchange_in, current_user_id=current_user.id)

    return Response(message="", data=exchange)
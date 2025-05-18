from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, crud


def update_fulfillment_service(
    db: Session,
    fulfillment_id: int,
    fulfillment_in: schemas.FulfillmentUpdate
) -> models.Fulfillment:
    fulfillment = crud.fulfillment.get(db, id=fulfillment_id)
    if not fulfillment:
        raise HTTPException(
            status_code=404,
            detail="The fulfillment does not exist in the system."
        )

    fulfillment = crud.fulfillment.update(db, db_obj=fulfillment, obj_in=fulfillment_in)

    # Attach consignment (if needed by response schema)
    fulfillment.consignment = crud.consignment.get(db, id=fulfillment.consignment_id)

    return fulfillment
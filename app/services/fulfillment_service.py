from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, crud


def update_fulfillment_service(
    db: Session,
    fulfillment_id: int,
    fulfillment_in: schemas.FulfillmentUpdate,
    updated_by : int
) -> models.Fulfillment:
    fulfillment = crud.fulfillment.get(db, id=fulfillment_id)
    if not fulfillment:
        raise HTTPException(
            status_code=404,
            detail="The fulfillment does not exist in the system."
        )

    update_data = fulfillment_in.model_dump(exclude_unset=True)
    update_data["user_id"] = updated_by

    fulfillment = crud.fulfillment.update(
        db=db,
        db_obj=fulfillment,
        obj_in=update_data
    )

    fulfillment.consignment = crud.consignment.get(db, id=fulfillment.consignment_id)
    return fulfillment
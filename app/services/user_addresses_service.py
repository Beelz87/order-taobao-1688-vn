from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.utils.roles import get_user_id_from_role


def update_user_address_service(
    db: Session,
    user_address_id: int,
    address_in: schemas.UserAddressUpdate,
    current_user: models.User,
    user_id: Optional[int] = None,
) -> models.UserAddress:
    final_user_id = get_user_id_from_role(current_user, user_id)

    user_address = crud.user_address.get(db, user_address_id)
    if not user_address:
        raise HTTPException(status_code=404, detail="The user address does not exist in the system.")

    if user_address.user_id != final_user_id:
        raise HTTPException(status_code=403, detail="You do not have permission to update this address.")

    updated_address = crud.user_address.update(db, db_obj=user_address, obj_in=address_in, user_id=final_user_id)
    return updated_address
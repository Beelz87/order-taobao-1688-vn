from typing import List, Union, Dict, Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user_address import UserAddress
from app.schemas.user_address import UserAddressCreate, UserAddressUpdate


class CRUDUserAddress(CRUDBase[UserAddress, UserAddressCreate, UserAddressUpdate]):
    def create(self, db: Session, *, obj_in: UserAddressCreate, **kwargs) -> UserAddress:
        user_id = kwargs.get("user_id")
        if user_id is None:
            raise ValueError("user_id is required for create operation")

        db_obj = UserAddress(
            user_id=user_id,
            name=obj_in.name,
            phone_number=obj_in.phone_number,
            address=obj_in.address,
            is_active=obj_in.is_active if obj_in.is_active is not None else True
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: UserAddress,
        obj_in: Union[UserAddressUpdate, Dict[str, Any]],
        **kwargs: Any
    ) -> UserAddress:
        user_id = kwargs.get("user_id")
        if user_id is None:
            raise ValueError("user_id is required for update operation")

        if db_obj.user_id != user_id:
            raise ValueError("Cannot update user address for a different user")

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


user_address = CRUDUserAddress(UserAddress)
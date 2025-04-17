from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session, joinedload

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(self.model).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate, **kwargs) -> User:
        db_obj = User(
            email=obj_in.email,
            user_code=obj_in.email.split("@")[0],
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            account_id=obj_in.account_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]],
        **kwargs: Any
    ) -> User:
        if obj_in.user_code != db_obj.user_code:
            if db_obj.is_user_code_edited:
                raise ValueError("user_code is edited before and cannot be changed anymore.")

            obj_in.is_user_code_edited = True

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def get(self, db: Session, *, id: int) -> Optional[User]:
        return db.query(self.model).options(
            joinedload(User.user_addresses),
            joinedload(User.user_finance)
        ).filter(User.id == id).first()

    def get_by_account_id(
        self,
        db: Session,
        *,
        account_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[User]:
        return (
            db.query(self.model)
            .filter(User.account_id == account_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


user = CRUDUser(User)

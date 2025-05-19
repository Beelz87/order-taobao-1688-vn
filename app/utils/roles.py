from typing import Optional

from fastapi import HTTPException

from app import models
from app.constants.role import Role


def get_user_id_from_role(
    current_user: models.User,
    user_id: Optional[int]
) -> int:
    if current_user.user_role.role.name == Role.USER["name"]:
        return current_user.id
    elif current_user.user_role.role.name in [Role.ADMIN["name"], Role.SUPER_ADMIN["name"]]:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required for admins")
        return user_id
    else:
        raise HTTPException(status_code=403, detail="Unauthorized role")
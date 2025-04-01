from typing import Optional

from pydantic import BaseModel

from app.schemas.role import Role


# Shared properties
class UserRoleBase(BaseModel):
    user_id: Optional[int]
    role_id: Optional[int]


# Properties to receive via API on creation
class UserRoleCreate(UserRoleBase):
    pass


# Properties to receive via API on update
class UserRoleUpdate(BaseModel):
    role_id: int


class UserRoleInDBBase(UserRoleBase):
    role: Role

    class Config:
        from_attributes = True


# Additional properties to return via API
class UserRole(UserRoleInDBBase):
    pass


class UserRoleInDB(UserRoleInDBBase):
    pass

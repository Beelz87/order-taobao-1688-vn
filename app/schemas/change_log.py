from typing import Dict, Any, List

from pydantic import BaseModel
from datetime import datetime


class ChangeLogBase(BaseModel):
    user_id: int
    object_type: str
    object_id: int
    action: str
    changes: List[Dict[str, Any]]
    created_at: datetime | None = None


class ChangeLogCreate(ChangeLogBase):
    pass


class ChangeLogInDBBase(ChangeLogBase):
    id: int

    class Config:
        from_attributes = True


# Additional properties to return via API
class ChangeLog(ChangeLogInDBBase):
    pass


# Additional properties stored in DB
class ChangeLogInDB(ChangeLogInDBBase):
    pass
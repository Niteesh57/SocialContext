from pydantic import BaseModel,field_validator
from datetime import date
from uuid import UUID

class RoleCreate(BaseModel):
    roleName: str
    createdAt: date = None
    modifiedAt: date = None

    class Config:
        orm_mode = True

    @field_validator('roleName')
    def validate_role_name(cls, v: str):
        if len(v) < 3:
            raise ValueError('Role name must be at least 3 characters long.')
        return v

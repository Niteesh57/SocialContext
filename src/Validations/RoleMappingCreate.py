from pydantic import BaseModel, field_validator
from uuid import UUID
from typing import Optional
from datetime import date

class RoleMappingCreate(BaseModel):
    roleId: UUID
    userId: int
    createdAt: Optional[date] = None
    modifiedAt: Optional[date] = None

    class Config:
        orm_mode = True

    @field_validator('roleId')
    def validate_role(cls, v: UUID):
        if v is None:
            raise ValueError('roleId cannot be None')
        return v
    
    @field_validator('userId')
    def validate_user(cls, v: int):
        if v is None:
            raise ValueError('userId cannot be None')
        return v

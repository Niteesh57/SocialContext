from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import date
from typing import Optional

class PostCreate(BaseModel):
    title: str
    content: str
    userId: int
    createdAt: Optional[date] = None
    modifiedAt: Optional[date] = None

    class Config:
        orm_mode = True  

    
    @field_validator('title')
    def validate_title(cls, v: str):
        if not v:
            raise ValueError('title cannot be empty')
        if len(v) > 500:
            raise ValueError('title cannot be longer than 500 characters')
        return v
    

    @field_validator('content')
    def validate_content(cls, v: str):
        if not v:
            raise ValueError('content cannot be empty')
        if len(v) > 3000:
            raise ValueError('content cannot be longer than 3000 characters')
        return v
    
    @field_validator('userId')
    def validate_user_id(cls, v: UUID):
        if v is None:
            raise ValueError('userId cannot be None')
        return v

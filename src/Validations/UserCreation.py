from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
import re

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('username')
    def validate_username(cls, v):
        if not v.isalnum() or len(v) < 3:
            raise ValueError('Username must be alphanumeric and at least 3 characters long')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Za-z]', v) or not re.search(r'\d', v):
            raise ValueError('Password must contain both letters and digits')
        return v

    class Config:
        orm_mode = True

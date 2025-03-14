from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException

class LoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        if len(value) > 100:
            raise ValueError("Username must be at most 100 characters long.")
        return value


    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return value

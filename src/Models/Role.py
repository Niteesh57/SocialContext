from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from datetime import date
from typing import List


class Role(SQLModel, table=True):
    __tablename__ = "role"
    
    id: UUID = Field(primary_key=True, unique=True)
    roleName: str
    createdAt: date
    modifiedAt: date

    role_mappings: List["RoleMapping"] = Relationship(back_populates="role")

def create_table(engine):
    Role.metadata.create_all(engine)

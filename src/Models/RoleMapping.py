from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from datetime import date

class RoleMapping(SQLModel, table=True):
    __tablename__ = "roleMapping"
    
    id: int = Field(default=None, primary_key=True)
    roleId: UUID = Field(foreign_key="role.id")
    userId: int = Field(foreign_key="user.id")
    createdAt: date
    modifiedAt: date


    user: "User" = Relationship(back_populates="role_mappings", sa_relationship_kwargs={"uselist": False})
    role: "Role" = Relationship(back_populates="role_mappings", sa_relationship_kwargs={"uselist": False})


def create_table(engine):
    RoleMapping.metadata.create_all(engine)


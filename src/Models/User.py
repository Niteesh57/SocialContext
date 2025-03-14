from sqlmodel import Field, SQLModel, Relationship
from datetime import date
from typing import List
# from dbConnection import engine
class User(SQLModel, table=True):
    __tablename__ = "user"
    
    id: int = Field(primary_key=True)
    username: str = Field(max_length=255, unique=True)
    email: str = Field(max_length=255)
    password: str = Field(max_length=255)
    createdAt: date
    modifiedAt: date

    role_mappings: List["RoleMapping"] = Relationship(back_populates="user")
    posts: List["Post"] = Relationship(back_populates="user")

def create_table():
    User.metadata.create_all(engine)

if __name__ == "__main__":
    create_table()
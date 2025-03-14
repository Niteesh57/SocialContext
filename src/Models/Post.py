from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from datetime import date
import uuid
# from dbConnection import engine

class Post(SQLModel, table=True):
    __tablename__ = "posts"
    
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=500, unique=True)
    content: str = Field(max_length=3000)
    createdAt: date = Field(default_factory=date.today)
    modifiedAt: date = Field(default_factory=date.today)
    
    userId: int = Field(foreign_key="user.id")

    user: "User" = Relationship(back_populates="posts")

def create_table():
    Post.metadata.create_all(engine)

if __name__ == "__main__":
    create_table()
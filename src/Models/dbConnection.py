import os
from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(os.getenv('POSTGRESQL_DATABASE_URL'), echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# from Role import Role
# from User import User
# from Post import Post
# from RoleMapping import RoleMapping

# Uncomment Above and do Migrations and Comment and run

def init_db():
    SQLModel.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()





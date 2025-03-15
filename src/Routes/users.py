from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.Models.dbConnection import SessionLocal
from src.Models.Role import Role
from src.Models.User import User
from src.Models.Post import Post
from src.Models.RoleMapping import RoleMapping
from src.Validations.UserCreation import UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from src.Security import Hash, Jwt 
from typing import List
from src.Security.auth import get_db, get_current_user, is_admin
from datetime import date
from uuid import uuid4

router = APIRouter()

@router.get("/usersAll", response_model=List[User], status_code=200, dependencies=[Depends(is_admin)])
async def get_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    users = db.query(User).all()
    db.close()
    return users

@router.post('/login', summary="Authenticate user and generate access token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not Hash.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    role_names = [role_mapping.role.roleName for role_mapping in user.role_mappings]
    
    access_token = Jwt.create_access_token(
        data={
            "sub": user.username,
            "role": role_names[0] if role_names else "user"
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



@router.post("/", response_model=User, summary="Create User", status_code=201, dependencies=[Depends(is_admin)])
async def create_user(user_create: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_user = db.query(User).filter(User.username == user_create.username).first()
    email_existing = db.query(User).filter(User.email == user_create.email).first()

    if existing_user or email_existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "User already registered"
        )
    
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        password=Hash.get_password_hash(user_create.password),  
        createdAt=date.today(),
        modifiedAt=date.today()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return assign_user_role(new_user, db)

def assign_user_role(new_user, db: Session):
    add_role = db.query(Role).filter(Role.roleName == 'User').first()
    if not add_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Default role 'User' not found"
        )

    new_role_mapping = RoleMapping(
        userId=new_user.id,
        roleId=add_role.id,
        createdAt=date.today(),
        modifiedAt=date.today()
    )

    db.add(new_role_mapping)
    db.commit()  
    db.refresh(new_role_mapping)
    return new_user


@router.put("/{user_id}", summary="Update user details", response_model=User, dependencies=[Depends(is_admin)])
async def update_user(user_id: int, username: str = None, email: str = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if username:
        user.username = username
    if email:
        user.email = email

    user.modifiedAt = date.today()
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", summary="Delete user", dependencies=[Depends(is_admin)])
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.query(RoleMapping).filter(RoleMapping.userId == user_id).delete()
    db.query(Post).filter(Post.userId == user_id).delete()

    db.delete(user)
    db.commit()

    return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="User deleted successfully")

@router.get("/usersById/{id}", status_code=200, response_model=User, summary="Get user by ID", dependencies=[Depends(is_admin)])
async def get_users_by_id(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"user with {id} not found"
        )
    
    role_names = [role_mapping.role.roleName for role_mapping in user.role_mappings]

    return {
        "user": user,
        "roles": role_names
    }
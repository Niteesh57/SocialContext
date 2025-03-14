from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.Models.dbConnection import SessionLocal
from src.Models.Role import Role
from src.Models.User import User
from src.Models.Post import Post
from src.Models.RoleMapping import RoleMapping
from src.Validations.RoleCreate import RoleCreate
from src.Security.auth import get_db, is_admin, get_current_user
from datetime import date
from typing import List
from uuid import uuid4, UUID

router = APIRouter()

@router.get("/rolesAll", response_model=List[Role], status_code=200, dependencies=[Depends(is_admin)])
async def get_role(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    role = db.query(Role).all()
    db.close()
    return role


@router.post("/", response_model=Role, status_code=201, dependencies=[Depends(is_admin)])
async def create_role(role_create: RoleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_role = db.query(Role).filter(Role.roleName == role_create.roleName).first()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already exists"
        )
    
    new_role = Role(
        id=uuid4(),
        roleName=role_create.roleName,
        createdAt=role_create.createdAt or date.today(),
        modifiedAt=role_create.modifiedAt or date.today()
    )

    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    db.close()
    return new_role

@router.get("/usersByRole/{role_name}", status_code=200, dependencies=[Depends(is_admin)])
async def get_users_by_role(role_name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    role = db.query(Role).filter(Role.roleName == role_name).first()
    
    if not role:
        raise HTTPException(
            status_code=404,
            detail=f"Role with name {role_name} not found"
        )
    
    role_mappings = role.role_mappings

    users_in_role = [mapping.user for mapping in role_mappings]

    if not users_in_role:
        raise HTTPException(
            status_code=404,
            detail=f"No users found for the role {role_name}"
        )

    return users_in_role

@router.delete("/{role_id}", summary="Delete role and associated users/posts", dependencies=[Depends(is_admin)])
async def delete_role(role_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    role_mappings = db.query(RoleMapping).filter(RoleMapping.roleId == role_id).all()
    user_ids = [mapping.userId for mapping in role_mappings]

    db.query(RoleMapping).filter(RoleMapping.roleId == role_id).delete()
    db.query(Post).filter(Post.userId.in_(user_ids)).delete()
    db.query(User).filter(User.id.in_(user_ids)).delete()

    db.delete(role)
    db.commit()

    return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Role, associated users, role mappings, and posts deleted successfully.")



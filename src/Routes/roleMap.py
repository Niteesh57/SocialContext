from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.Models.dbConnection import SessionLocal
from src.Models.Role import Role
from src.Models.User import User
from src.Models.Post import Post
from src.Models.RoleMapping import RoleMapping
from src.Validations.RoleMappingCreate import RoleMappingCreate
from src.Security.auth import get_db, get_current_user, is_admin
from datetime import date
from typing import List
from uuid import uuid4

router = APIRouter()

@router.get("/rolesMapAll", status_code=200, response_model=List[RoleMapping], dependencies=[Depends(is_admin)])
async def get_roleMap(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    roleMap = db.query(RoleMapping).all()
    db.close()
    return roleMap


@router.post("/role-mappings", response_model=RoleMapping, status_code=201, dependencies=[Depends(is_admin)])
async def create_role_mapping(role_mapping_create: RoleMappingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    role = db.query(Role).filter(Role.id == role_mapping_create.roleId).first()
    user = db.query(User).filter(User.id == role_mapping_create.userId).first()
    if not role or not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail =  "Role not found"
        )
    
    new_role_mapping = RoleMapping(
        roleId=role_mapping_create.roleId,
        userId=role_mapping_create.userId,
        createdAt=role_mapping_create.createdAt or date.today(),
        modifiedAt=role_mapping_create.modifiedAt or date.today()
    )

    db.add(new_role_mapping)
    db.commit()
    db.refresh(new_role_mapping)
    db.close()
    return new_role_mapping



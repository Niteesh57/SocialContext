from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.Models.dbConnection import SessionLocal
from src.Models.Post import Post
from src.Models.User import User
from uuid import uuid4, UUID
from typing import List
from src.Validations.PostCreate import PostCreate
from src.Security.auth import get_db, get_current_user, is_admin
from datetime import date

router = APIRouter()

@router.get("/postsAll", response_model=List[Post], status_code=200)
async def get_post(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    posts = db.query(Post).all()
    db.close()
    return posts

@router.get("/posts/{userId}/user", response_model=List[Post], status_code=200, dependencies=[Depends(is_admin)])
async def get_posts_by_user(userId: int,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == userId).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user.posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User has no posts")
    return user.posts

@router.post("/post-create", status_code=201, response_model=Post, dependencies=[Depends(is_admin)])
async def create_post(post_create: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == post_create.userId).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    post = Post(
        title=post_create.title,
        content=post_create.content,
        userId=post_create.userId,
        createdAt=post_create.createdAt or date.today(),
        modifiedAt=post_create.modifiedAt or date.today()
    )

    db.add(post)
    db.commit()
    db.refresh(post)
    db.close()
    return post 

@router.get("/{post_id}", summary="Get post by ID", response_model=Post, dependencies=[Depends(is_admin)])
async def get_post_by_id(post_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return post

@router.put("/{post_id}", summary="Update post", response_model=Post, dependencies=[Depends(is_admin)])
async def update_post(post_id: UUID, title: str = None, content: str = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if title:
        post.title = title
    if content:
        post.content = content

    post.modifiedAt = date.today()
    db.commit()
    db.refresh(post)

    return post

@router.delete("/{post_id}", summary="Delete post", dependencies=[Depends(is_admin)])
async def delete_post(post_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    db.delete(post)
    db.commit()

    return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Post deleted successfully")
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowPassword
from fastapi.security import OAuth2
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.Models import User
from src.Models.dbConnection import SessionLocal
from src.Security import Jwt
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login",
    scheme_name="JWT"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = Jwt.decode_jwt(token)
    username: str = payload.get("sub")
    role: str = payload.get("role")

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid"
        )
    user = db.query(User.User).filter(User.User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"user": user, "role": role}


def is_admin(current_user: dict = Depends(get_current_user)):
    print('hi')
    if current_user["role"] != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Admins only")
    return current_user
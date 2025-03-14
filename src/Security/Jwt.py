import jwt
import os
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from dotenv import load_dotenv
from typing import Union, Any, Dict
from jose import jwt

load_dotenv()

def create_access_token(data: Dict[str, str], expires_in: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=int(expires_in))
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY") , algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

from jose import jwt
from sqlalchemy import select
from database.models import User
from fastapi import status, Request
from data.config import get_auth_data
from database.core import AsyncSession
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from datetime import datetime, timedelta, timezone
from database.core import UserRepository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def check_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')    
    try:
        jwt.decode(token, get_auth_data()['secret_key'], get_auth_data()['algorithm'])
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
    

async def authenticate_user(password: str, hashed_password: str,  session: AsyncSession) -> User:
    if not verify_password(plain_password=password, hashed_password=hashed_password):
        return None
    return 'Success'
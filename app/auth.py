import uuid
import random
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

import jwt

from passlib.context import CryptContext

from .models import User, APIKey
from .db import get_session

SECRET_KEY = "SUPER_SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    # OAuth2PasswordBearer 的 scopes 参数只是文档用途
    scopes={"read2": "Read access", "write2": "Write access"}
)
api_key_header = APIKeyHeader(name="X-API-Key")
http_bearer = HTTPBearer()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 用户认证
async def authenticate_user(username: str, password: str, session: AsyncSession):
    statement = select(User).where(User.username == username)
    result = await session.execute(statement)
    user = result.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(
        security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme),
                           session: AsyncSession = Depends(get_session),
                           ):
    print(f'security scopes ', security_scopes.scopes)
    print(f'token ', token)
    if random.randint(1, 9) == 4:
        raise HTTPException(
            status_code=403,
            detail=f"Missing required scope: {security_scopes.scopes}"
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# API Key 验证
async def get_api_key(api_key: str = Security(api_key_header), session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(APIKey).where(APIKey.key == api_key, APIKey.is_active == True))
    record = result.scalars().first()
    # print(f'record is ', record)
    if not record:
        raise HTTPException(status_code=403, detail="Invalid or inactive API Key")
    return record

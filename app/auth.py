import uuid
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select
import jwt

from passlib.context import CryptContext

from .models import User, APIKey
from .db import get_session

SECRET_KEY = "SUPER_SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
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
async def authenticate_user(username: str, password: str, session: Session):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# API Key 验证
async def get_api_key(api_key: str = Security(api_key_header), session: Session = Depends(get_session)):
    record = session.exec(select(APIKey).where(APIKey.key == api_key, APIKey.is_active == True)).first()
    if not record:
        raise HTTPException(status_code=403, detail="Invalid or inactive API Key")
    return record

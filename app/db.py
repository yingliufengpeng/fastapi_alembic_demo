from typing import AsyncGenerator
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlmodel import SQLModel
# 异步 Engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.orm import sessionmaker

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# SQLALCHEMY_DATABASE_URL = f"sqlite:///{BASE_DIR / 'app.db'}"
SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{BASE_DIR / 'app.db'}"



engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,              # 打印 SQL 日志
    future=True
)

# 异步 session
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
async def get_session() -> AsyncGenerator :
    async with AsyncSessionLocal() as session:
        yield session


Base = SQLModel



import anyio
import uuid
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi import Security

from sqlmodel.ext.asyncio.session import AsyncSession

# from app.models import User
from ..models import User

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

router = APIRouter()
from ..auth import get_current_user
from ..db import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/user-data")
async def read_user_data(user: User = Depends(get_current_user)):
    return {"msg": f"Hello {user.username}, protected user data"}

@router.get("/users/me")
async def read_own_user(
        current_user = Security(get_current_user, scopes=["read"])
):
    return current_user

@router.get("/users/")
async def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    result = await session.execute(select(User).offset(offset).limit(limit))
    users = result.scalars().all()  # ✅ 直接得到 User 对象列表
    return users

@router.post("/users/")
async def create_user(user: User, session: SessionDep) :
    print('user is ', user)
    session.add(user)
    await session.commit()
    session.refresh(user)
    return user


@router.delete("/users/{user_id}")
async def delete_hero(user_id: uuid.UUID, session: SessionDep):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)  # ✅ AsyncSession 也支持 await delete()
    await session.commit()
    return {"ok": True}


@router.patch("/users/{user_id}", response_model=User)
async def update_hero(user_id: uuid.UUID, user: User, session: SessionDep):
    user_db = await session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    await session.commit()
    session.refresh(user_db)
    return user_db


@router.get("/users/{user_id}")
async def read_hero(user_id: uuid.UUID, session: SessionDep) -> User:
    # user = await session.get(User, user_id)
    print(f' user_id is {user_id}')
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 定义一个异步生成器，产生流式数据
async def number_stream():
    for i in range(10):
        await anyio.sleep(1)   # 模拟耗时任务
        yield f"data: {i}\n"   # 每次返回一条消息（Server-Sent Events 格式）

# 路由返回流式响应
@router.get("/stream")
async def stream_numbers():
    return StreamingResponse(number_stream(), media_type="text/event-stream")
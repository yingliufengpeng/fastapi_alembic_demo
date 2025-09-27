
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

import anyio
from app.models import User

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

router = APIRouter()

from app.db import get_session

SessionDep = Annotated[Session, Depends(get_session)]


# Code above omitted 👆

@router.get("/users/")
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:

    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return list(users)

# Code below omitted 👇


# Code above omitted 👆

@router.post("/users/")
def create_user(user: User, session: SessionDep) :
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Code above omitted 👆

@router.delete("/users/{user_id}")
def delete_hero(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}


@router.patch("/users/{user_id}", response_model=User)
def update_hero(user_id: int, user: User, session: SessionDep):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

# Code below omitted 👇

@router.get("/users/{user_id}")
def read_hero(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
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
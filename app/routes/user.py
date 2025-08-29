
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
 
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
    # breakpoint()
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

# Code below omitted 👇


# Code above omitted 👆

@router.post("/users/")
def create_user(user: User, session: SessionDep) -> None:
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

# Code above omitted 👆


# Code above omitted 👆

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

# Code below omitted 👇

# Code below omitted 👇
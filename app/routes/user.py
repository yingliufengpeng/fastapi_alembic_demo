
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

# Code below omitted 👇
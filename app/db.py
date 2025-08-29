 
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlmodel import SQLModel

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SQLALCHEMY_DATABASE_URL = f"sqlite:///{BASE_DIR / 'app.db'}"


print(f' sqlite path is {BASE_DIR/"app.db"}' )

 
engine = create_engine(
            SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
            )


def get_session():
    with Session(engine) as session:
        yield session

Base = SQLModel


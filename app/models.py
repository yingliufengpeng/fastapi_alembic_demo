from typing import List, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
import uuid
from sqlalchemy import Column, String

class Company(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int = Field(index=True)

class Base(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)


class Category(Base, table=True):
    tag: str
     # 反向关系（一个分类有多个商品）
    items: List["Item"] = Relationship(back_populates="category", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
 
class Item(Base, table=True):
    description: str
    category_id: int | None = Field(default=None, foreign_key="category.id")

    # 正向关系（一个商品属于一个分类）
    category: Optional[Category] = Relationship(back_populates="items")

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = 'user1'
    hashed_password: str  = ''
    is_active: bool = True
    age: int | None = Field(default=None, index=True)
    secret_name: str
    category_id: int | None = Field(default=None, foreign_key="category.id")

class APIKey(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    key: str = Field(index=True, nullable=False, unique=True)  # 真实项目建议存哈希
    owner: str
    is_active: bool = True
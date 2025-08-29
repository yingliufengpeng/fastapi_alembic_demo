from sqlalchemy import Column, Integer, String
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Company(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int = Field(index=True)

class Base(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)


class Category(Base, table=True):
    tag: str
    
 
class Item(Base, table=True):
    description: str
    category_id: int | None = Field(default=None, foreign_key="category.id")

class User(Base, table=True):
  
    age: int | None = Field(default=None, index=True)
    secret_name: str
   

    category_id: int | None = Field(default=None, foreign_key="category.id")


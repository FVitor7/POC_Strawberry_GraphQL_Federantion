from typing import Optional

import sqlalchemy
from database.database import Base
from database.settings import DATABASE_URL
from databases import Database
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

metadata = sqlalchemy.MetaData()


class Category(Base):
    __tablename__ = "categories"
    metadata
    id: int = Column(Integer, primary_key=True, index=True)
    category_name: str = Column(String, nullable=False, unique=True)

    tasks: list["Task"] = relationship("Task", lazy="joined", back_populates="category")


class Task(Base):
    __tablename__ = "tasks"
    metadata
    id: int = Column(Integer, primary_key=True, index=True)
    task_name: str = Column(String, nullable=False, unique=True)

    user_id: int = Column(Integer, nullable=True)

    category_id: Optional[int] = Column(Integer, ForeignKey(Category.id), nullable=True)
    category: Optional[Category] = relationship(Category, lazy="joined", back_populates="tasks")


database = Database(DATABASE_URL)

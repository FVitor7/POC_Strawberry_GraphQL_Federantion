import sqlalchemy
from database.database import Base
from database.settings import DATABASE_URL
from databases import Database
from sqlalchemy import Column, Integer, String

metadata = sqlalchemy.MetaData()


class User(Base):
    __tablename__ = "users"
    metadata
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False, unique=False)
    email: str = Column(String, nullable=False, unique=True)
    cpf: str = Column(String, nullable=True, unique=True)


database = Database(DATABASE_URL)

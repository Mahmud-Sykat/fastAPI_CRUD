from sqlalchemy import Column, Integer, String
from database import Base

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)       
    description = Column(String(500))            

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)    
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

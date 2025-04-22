from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Text
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    
class FileProcessing(Base):
    __tablename__ = "file_processing"
    
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(100))
    status = Column(String(100), default="pending")  # pending, processing, completed, failed
    result = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    popularity = Column(Integer, index=True,nullable=True)
    sales=Column(String(200))
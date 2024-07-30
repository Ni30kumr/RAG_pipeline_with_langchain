from sqlalchemy import create_engine, Column, Integer, String, Text,JSON
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))
    bot_config = Column(JSON, comment="Stores PDF path and Pinecone index name as JSON")
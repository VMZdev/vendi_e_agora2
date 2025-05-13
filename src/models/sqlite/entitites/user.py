from sqlalchemy import Column, Integer, String
from src.models.sqlite.settings.base import Base

class UserTable(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")
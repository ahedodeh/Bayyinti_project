from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SqlEnum, DateTime, func
from datetime import datetime
from app.database import Base
from app.enum.user_role import UserRole

class User(Base):
    __tablename__ = "users"

    UserId = Column(Integer, primary_key=True, index=True)
    Email = Column(String, unique=True, nullable=False, index=True)
    Phone = Column(String, unique=True, nullable=True)
    FullName = Column(String, nullable=True)
    Password = Column(String, nullable=True) 
    Role = Column(SqlEnum(UserRole), default=UserRole.STD)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr
from .database import Base
import datetime
from datetime import UTC

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="user")  # user, staff, admin
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(UTC))
    activity_logs = relationship("ActivityLog", back_populates="user")


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str  # Should be "user" or "admin"

class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    department = Column(String(100))
    user = relationship("User")

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    privileges = Column(String(255), default="full_access")
    user = relationship("User")

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(255))
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(UTC))
    details = Column(String(255))
    user = relationship("User", back_populates="activity_logs")

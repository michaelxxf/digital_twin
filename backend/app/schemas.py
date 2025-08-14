from pydantic import BaseModel, EmailStr
from typing import Optional, List
import datetime

class ActivityLogBase(BaseModel):
    action: str
    details: Optional[str] = None

class ActivityLogCreate(ActivityLogBase):
    pass

class ActivityLog(ActivityLogBase):
    id: int
    timestamp: datetime.datetime
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    is_active: bool
    role: str
    created_at: datetime.datetime
    activity_logs: List[ActivityLog] = []
    class Config:
        orm_mode = True

class StaffBase(BaseModel):
    department: Optional[str] = None

class StaffCreate(StaffBase):
    user_id: int

class Staff(StaffBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True

class AdminBase(BaseModel):
    privileges: Optional[str] = None

class AdminCreate(AdminBase):
    user_id: int

class Admin(AdminBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True

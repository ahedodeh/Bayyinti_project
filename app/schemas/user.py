from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.enum.user_role import UserRole

class UserBase(BaseModel):
    Email: EmailStr
    Phone: Optional[str] = None
    FullName: Optional[str] = None
    Role: Optional[UserRole] = UserRole.STD

class UserCreate(UserBase):
    Password: Optional[str] = None  

class UserUpdate(BaseModel):
    Email: Optional[EmailStr] = None
    Phone: Optional[str] = None
    FullName: Optional[str] = None
    Password: Optional[str] = None
    Role: Optional[UserRole] = None

class UserOut(UserBase):
    UserId: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }

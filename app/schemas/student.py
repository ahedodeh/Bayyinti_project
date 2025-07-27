from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.enum.student_enums import CollegeEnum, DegreeEnum

class StudentBase(BaseModel):
    college: CollegeEnum
    specialization: str
    university_campus: str
    date_of_birth: date
    degree: DegreeEnum
    gender: str
    user_id: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    college: Optional[CollegeEnum] = None
    specialization: Optional[str] = None
    university_campus: Optional[str] = None
    date_of_birth: Optional[date] = None
    degree: Optional[DegreeEnum] = None
    gender: Optional[str] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True

class StudentOut(StudentBase):
    id: int
    class Config:
        orm_mode = True

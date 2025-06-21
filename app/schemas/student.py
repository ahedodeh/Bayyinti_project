from pydantic import BaseModel

class StudentBase(BaseModel):
    user_id: int

class StudentCreate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int

    class Config:
        orm_mode = True

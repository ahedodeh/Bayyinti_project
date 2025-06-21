from pydantic import BaseModel

class BookingBase(BaseModel):
    bed_id: int
    student_id: int

class BookingCreate(BookingBase):
    pass

class BookingOut(BookingBase):
    id: int

    class Config:
        orm_mode = True

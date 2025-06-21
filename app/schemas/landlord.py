from pydantic import BaseModel

class LandlordBase(BaseModel):
    user_id: int

class LandlordCreate(LandlordBase):
    pass

class LandlordOut(LandlordBase):
    id: int

    class Config:
        orm_mode = True

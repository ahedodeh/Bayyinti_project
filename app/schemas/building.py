from pydantic import BaseModel

class BuildingBase(BaseModel):
    name: str
    address: str
    landlord_id: int

class BuildingCreate(BuildingBase):
    pass

class BuildingOut(BuildingBase):
    id: int

    class Config:
        orm_mode = True

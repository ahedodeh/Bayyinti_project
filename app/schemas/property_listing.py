from pydantic import BaseModel
from typing import Optional
from app.schemas.room import RoomResponse  # إذا أردت ترجع الغرف نفسها أيضًا


class PropertyListingCreate(BaseModel):
    building_name: Optional[str]
    building_number: Optional[str]
    landlord_id: int
    title: Optional[str]
    description: Optional[str]
    floor_number: Optional[int]
    location_lat: Optional[float]
    location_lon: Optional[float]
    is_active: Optional[bool] = True
    gender_preference: Optional[str]
    has_gas: Optional[bool] = False
    has_electricity: Optional[bool] = False
    has_water: Optional[bool] = False
    has_internet: Optional[bool] = False


class PropertyListingResponse(PropertyListingCreate):
    id: int
    number_of_rooms: int  

    class Config:
        orm_mode = True

from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.enum.city import CityEnum
from app.enum.country import CountryEnum

class PropertyListingCreate(BaseModel):
    building_name: Optional[str]
    building_number: Optional[str]
    landlord_id: str
    title: Optional[str]
    description: Optional[str]
    floor_number: Optional[int]
    location_lat: Optional[str]
    location_lon: Optional[str]
    is_active: Optional[bool] = True
    gender_preference: Optional[str]
    has_gas: Optional[bool] = False
    has_electricity: Optional[bool] = False
    has_water: Optional[bool] = False
    has_internet: Optional[bool] = False
    property_type: Optional[str]
    property_image: Optional[str]
    city: Optional[CityEnum]
    country: Optional[CountryEnum]

class PropertyListingUpdate(BaseModel):
    building_name: Optional[str] = None
    building_number: Optional[str] = None
    landlord_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    floor_number: Optional[int] = None
    location_lat: Optional[str] = None
    location_lon: Optional[str] = None
    is_active: Optional[bool] = None
    gender_preference: Optional[str] = None
    has_gas: Optional[bool] = None
    has_electricity: Optional[bool] = None
    has_water: Optional[bool] = None
    has_internet: Optional[bool] = None
    property_type: Optional[str] = None
    property_image: Optional[str] = None
    city: Optional[CityEnum] = None
    country: Optional[CountryEnum] = None

class PropertyListingResponse(PropertyListingCreate):
    id: int
    number_of_rooms: Optional[int] = 0
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }

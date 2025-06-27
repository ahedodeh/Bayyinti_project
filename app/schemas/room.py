from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.enum.room_type_enum import RoomTypeEnum

class RoomBase(BaseModel):
    description: Optional[str]
    price_of_bed_per_month: Optional[float]
    available_from: Optional[date]
    is_active: Optional[bool] = True
    room_type: Optional[RoomTypeEnum]
    number_of_beds: Optional[int]
    number_of_available_beds: Optional[int]
    has_internal_bathroom: Optional[bool] = False
    has_internal_balcony: Optional[bool] = False
    has_ac: Optional[bool] = False
    has_office: Optional[bool] = False

class RoomCreate(RoomBase):
    property_listing_id: int

class RoomResponse(RoomBase):
    id: int
    property_listing_id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }

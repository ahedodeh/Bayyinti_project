# ✅ schemas/room.py

from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.Enums.room_type_enum import RoomTypeEnum


class RoomBase(BaseModel):
    description: Optional[str]
    price_of_bed_per_month: Optional[float]
    available_from: Optional[date]
    is_active: Optional[bool] = True
    room_type: Optional[RoomTypeEnum]
    number_of_beds: Optional[int]
    number_of_available_beds: Optional[int]

class RoomCreate(RoomBase):
    property_listing_id: int

class RoomResponse(RoomBase):
    id: int
    property_listing_id: int

    class Config:
        orm_mode = True
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.enums.shared_space_type_enum import SharedSpaceTypeEnum

class SharedSpaceBase(BaseModel):
    room_type: SharedSpaceTypeEnum
    description: Optional[str] = None

class SharedSpaceCreate(SharedSpaceBase):
    property_id: int

class SharedSpaceUpdate(SharedSpaceBase):
    pass

class SharedSpaceResponse(BaseModel):
    id: int
    property_id: int
    room_type: SharedSpaceTypeEnum
    description: Optional[str] = None
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }

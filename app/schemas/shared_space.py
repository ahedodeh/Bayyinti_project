from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.enum.shared_space_type_enum import SharedSpaceTypeEnum
from app.schemas.image import ImageResponse

class SharedSpaceBase(BaseModel):
    room_type: SharedSpaceTypeEnum
    description: Optional[str] = None

class SharedSpaceCreate(SharedSpaceBase):
    property_id: int

class SharedSpaceUpdate(BaseModel):
    room_type: Optional[SharedSpaceTypeEnum] = None
    description: Optional[str] = None
    image_ids_to_delete: Optional[List[int]] = None

class SharedSpaceResponse(BaseModel):
    id: int
    property_id: int
    room_type: SharedSpaceTypeEnum
    description: Optional[str] = None
    created_at: Optional[datetime]
    images: Optional[List[ImageResponse]] = None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }

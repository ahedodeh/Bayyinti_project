from pydantic import BaseModel, model_validator
from typing import Optional, List
from datetime import datetime
from app.enum.shared_space_type_enum import SharedSpaceTypeEnum
from app.schemas.image import ImageResponse
from app.config import BASE_URL

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

    @model_validator(mode="after")
    def generate_image_urls(self):
        if self.images:
            for image in self.images:
                if image.image_url and not image.image_url.startswith("http"):
                    clean_url = image.image_url.replace("\\", "/").lstrip("/")
                    image.image_url = f"{BASE_URL}/{clean_url}"
        return self

    class Config:
        from_attributes = True 
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }

from pydantic import BaseModel, field_serializer
from typing import Optional
from datetime import date, datetime
from app.enum.room_type_enum import RoomTypeEnum
from typing import List
from app.schemas.image import ImageResponse
from pydantic import model_validator
from app.config import BASE_URL  

class RoomBase(BaseModel):
    description: Optional[str]
    price_of_bed_per_month: Optional[float]
    available_from: Optional[date]
    is_active: Optional[bool] = True
    is_available: Optional[bool] = True
    room_type: Optional[RoomTypeEnum]
    number_of_beds: Optional[int]
    number_of_available_beds: Optional[int]
    has_internal_bathroom: Optional[bool] = False
    has_internal_balcony: Optional[bool] = False
    has_ac: Optional[bool] = False
    has_office: Optional[bool] = False

class RoomCreate(RoomBase):
    property_listing_id: int

class RoomResponse(BaseModel):
    id: int
    property_listing_id: int
    description: Optional[str]
    price_of_bed_per_month: Optional[float]
    available_from: Optional[date]
    room_type: Optional[RoomTypeEnum]
    number_of_beds: Optional[int]
    number_of_available_beds: Optional[int]
    created_at: Optional[datetime]
    images: Optional[List[ImageResponse]] = []

    is_active: Optional[bool] = False
    is_available: Optional[bool] = False
    has_internal_bathroom: Optional[bool] = False
    has_internal_balcony: Optional[bool] = False
    has_ac: Optional[bool] = False
    has_office: Optional[bool] = False

    @field_serializer(
        "is_active",
        "is_available",
        "has_internal_bathroom",
        "has_internal_balcony",
        "has_ac",
        "has_office",
        mode="plain"
    )
    def serialize_boolean(self, value: Optional[bool]) -> bool:
        return bool(value)

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
class RoomUpdate(BaseModel):
    description: Optional[str] = None
    price_of_bed_per_month: Optional[float] = None
    available_from: Optional[date] = None
    is_active: Optional[bool] = None
    is_available: Optional[bool] = None
    room_type: Optional[RoomTypeEnum] = None
    number_of_beds: Optional[int] = None
    number_of_available_beds: Optional[int] = None
    has_internal_bathroom: Optional[bool] = None
    has_internal_balcony: Optional[bool] = None
    has_ac: Optional[bool] = None
    has_office: Optional[bool] = None
    image_ids_to_delete: Optional[List[int]] = None


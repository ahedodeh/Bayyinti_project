from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ImageCreate(BaseModel):
    entity_id: int

class ImageResponse(BaseModel):
    id: int
    entity_id: int
    image_url: str
    created_at: Optional[str]  

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        data = obj.__dict__.copy()
        data['created_at'] = obj.created_at.strftime("%Y-%m-%d %H:%M:%S") if obj.created_at else None
        return cls(**data)

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ImageResponse(BaseModel):
    id: int
    entity_id: int
    entity_type: str
    image_url: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }

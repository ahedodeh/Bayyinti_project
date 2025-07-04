from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List
class ImageCreate(BaseModel):
    entity_id: int

class ImageResponse(BaseModel):
    id: int
    entity_id: int
    image_url: str
    created_at: Optional[datetime] 
    class Config:
        orm_mode = True

    class Config:
        from_attributes = True  
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }

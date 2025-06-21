# schemas/room_image.py

from pydantic import BaseModel
from typing import Optional

class RoomImageCreate(BaseModel):
    room_id: int

class RoomImageResponse(BaseModel):
    id: int
    room_id: int
    image_url: str

    class Config:
        orm_mode = True

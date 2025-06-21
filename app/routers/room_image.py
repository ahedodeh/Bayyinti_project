# routers/room_image.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
from uuid import uuid4

from app.database import get_db
from app.crud import room_image as crud
from app.schemas.room_image import RoomImageResponse

router = APIRouter(prefix="/room-images", tags=["Room Images"])

UPLOAD_DIR = "uploads/room_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=RoomImageResponse)
def upload_image(room_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = f"/{file_path}"  # for local path. You can adjust this if using cloud
    return crud.create_room_image(db, room_id=room_id, image_url=image_url)

@router.get("/{image_id}", response_model=RoomImageResponse)
def read_image(image_id: int, db: Session = Depends(get_db)):
    image = crud.get_image_by_id(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image

@router.get("/room/{room_id}", response_model=list[RoomImageResponse])
def read_images_by_room(room_id: int, db: Session = Depends(get_db)):
    return crud.get_images_by_room_id(db, room_id)

@router.delete("/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_image(db, image_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted"}

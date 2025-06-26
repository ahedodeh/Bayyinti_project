from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
from uuid import uuid4

from app.database import get_db
from app.crud import image as crud
from app.schemas.image import ImageResponse

router = APIRouter(prefix="/images", tags=["Images"])

UPLOAD_DIR = "uploads/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=ImageResponse)
def upload_image(entity_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = f"/{file_path}"
    image = crud.create_image(db, entity_id=entity_id, image_url=image_url)
    return ImageResponse.from_orm(image)

@router.get("/{image_id}", response_model=ImageResponse)
def read_image(image_id: int, db: Session = Depends(get_db)):
    image = crud.get_image_by_id(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return ImageResponse.from_orm(image)

@router.get("/entity/{entity_id}", response_model=list[ImageResponse])
def read_images_by_entity(entity_id: int, db: Session = Depends(get_db)):
    images = crud.get_images_by_entity_id(db, entity_id)
    return [ImageResponse.from_orm(img) for img in images]

@router.delete("/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_image(db, image_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted"}

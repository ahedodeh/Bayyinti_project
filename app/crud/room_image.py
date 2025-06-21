# crud/room_image.py

from sqlalchemy.orm import Session
from app.models.room_image import RoomImage

def create_room_image(db: Session, room_id: int, image_url: str):
    image = RoomImage(room_id=room_id, image_url=image_url)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

def get_image_by_id(db: Session, image_id: int):
    return db.query(RoomImage).filter(RoomImage.id == image_id).first()

def get_images_by_room_id(db: Session, room_id: int):
    return db.query(RoomImage).filter(RoomImage.room_id == room_id).all()

def delete_image(db: Session, image_id: int):
    image = get_image_by_id(db, image_id)
    if image:
        db.delete(image)
        db.commit()
    return image

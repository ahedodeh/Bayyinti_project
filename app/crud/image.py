# crud/image.py

from sqlalchemy.orm import Session
from app.models.image import Image

def create_image(db: Session, entity_id: int, image_url: str):
    image = Image(entity_id=entity_id, image_url=image_url)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

def get_image_by_id(db: Session, image_id: int):
    return db.query(Image).filter(Image.id == image_id).first()

def get_images_by_entity_id(db: Session, entity_id: int):
    return db.query(Image).filter(Image.entity_id == entity_id).all()

def delete_image(db: Session, image_id: int):
    image = get_image_by_id(db, image_id)
    if image:
        db.delete(image)
        db.commit()
    return image

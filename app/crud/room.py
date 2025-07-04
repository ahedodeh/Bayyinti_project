from sqlalchemy.orm import Session
from app.models.room import Room
from app.schemas.room import RoomCreate
from app.schemas.room import RoomUpdate

def create_room(db: Session, room_data: RoomCreate):
    room = Room(**room_data.dict())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

def get_room_by_id(db: Session, room_id: int):
    return db.query(Room).filter(Room.id == room_id).first()

def get_rooms_by_listing_id(db: Session, listing_id: int):
    return db.query(Room).filter(Room.property_listing_id == listing_id).all()

def update_room(db: Session, room_id: int, updates: RoomUpdate):
    room = db.query(Room).filter(Room.id == room_id).first()
    if room:
        for key, value in updates.dict(exclude_unset=True).items():
            setattr(room, key, value)
        db.commit()
        db.refresh(room)
    return room

def delete_room(db: Session, room_id: int):
    room = db.query(Room).filter(Room.id == room_id).first()
    if room:
        db.delete(room)
        db.commit()
    return room
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.room import RoomCreate, RoomResponse, RoomUpdate
from app.crud import room as room_crud

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create(room: RoomCreate, db: Session = Depends(get_db)):
    return room_crud.create_room(db, room)

@router.get("/{room_id}", response_model=RoomResponse)
def read(room_id: int, db: Session = Depends(get_db)):
    room = room_crud.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.get("/listing/{listing_id}", response_model=list[RoomResponse])
def get_by_listing(listing_id: int, db: Session = Depends(get_db)):
    return room_crud.get_rooms_by_listing_id(db, listing_id)

@router.put("/{room_id}", response_model=RoomResponse, summary="Partial Update")
def partial_update(room_id: int, updates: RoomUpdate, db: Session = Depends(get_db)):
    updated = room_crud.update_room(db, room_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Room not found")
    return updated

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(room_id: int, db: Session = Depends(get_db)):
    deleted = room_crud.delete_room(db, room_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Room not found")

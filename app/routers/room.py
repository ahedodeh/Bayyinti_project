from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.database import get_db
from app.schemas.room import RoomResponse,RoomUpdate
from app.models.image import Image
from app.models.room import RoomTypeEnum
from app.crud import room as room_crud
import os, uuid, shutil
from typing import Optional
from fastapi import Request


router = APIRouter(prefix="/rooms", tags=["Rooms"])


UPLOAD_DIR = "uploads/rooms"

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(
    property_listing_id: int = Form(...),
    description: str = Form(None),
    price_of_bed_per_month: float = Form(None),
    available_from: date = Form(None),
    is_active: bool = Form(True),
    is_available: bool = Form(True),
    room_type: RoomTypeEnum = Form(None),
    number_of_beds: int = Form(None),
    number_of_available_beds: int = Form(None),
    has_internal_bathroom: bool = Form(False),
    has_internal_balcony: bool = Form(False),
    has_ac: bool = Form(False),
    has_office: bool = Form(False),
    images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    from app.schemas.room import RoomCreate

    room_data = RoomCreate(
        property_listing_id=property_listing_id,
        description=description,
        price_of_bed_per_month=price_of_bed_per_month,
        available_from=available_from,
        is_active=is_active,
        is_available=is_available,
        room_type=room_type,
        number_of_beds=number_of_beds,
        number_of_available_beds=number_of_available_beds,
        has_internal_bathroom=has_internal_bathroom,
        has_internal_balcony=has_internal_balcony,
        has_ac=has_ac,
        has_office=has_office,
    )

    room = room_crud.create_room(db, room_data)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    if images:
       for image in images:
        ext = image.filename.split(".")[-1]
        file_name = f"{uuid.uuid4().hex}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_record = Image(entity_id=room.id, image_url=file_path)
        db.add(image_record)

    db.commit()
    room.images = db.query(Image).filter(Image.entity_id == room.id).all()

    return room 


@router.get("/{room_id}", response_model=RoomResponse)
def read(room_id: int, db: Session = Depends(get_db)):
    room = room_crud.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    room.images = db.query(Image).filter(Image.entity_id == room.id).all()
    return room

@router.get("/listing/{listing_id}", response_model=List[RoomResponse])
def get_by_listing(listing_id: int, db: Session = Depends(get_db)):
    rooms = room_crud.get_rooms_by_listing_id(db, listing_id)
    for room in rooms:
        room.images = db.query(Image).filter(Image.entity_id == room.id).all()
    return rooms


@router.put("/{room_id}", response_model=RoomResponse)
async def partial_update(
    room_id: int,
    request: Request,
    db: Session = Depends(get_db),
    images: Optional[List[UploadFile]] = File(None),
    image_ids_to_delete: Optional[str] = Form(None),
):
    import json
    from app.schemas.room import RoomUpdate
    from app.models.image import Image
    import os, uuid, shutil

    form = await request.form()
    update_data_dict = {}

    for key in RoomUpdate.__annotations__:
        if key in form and form[key] != "":
            value = form[key]
            field_type = RoomUpdate.__annotations__[key]

            # Handle booleans
            if field_type == bool:
                value = value.lower() in ["true", "1"]
            elif field_type == int:
                value = int(value)
            elif field_type == float:
                value = float(value)
            elif field_type == list:
                value = json.loads(value)
            elif field_type.__name__ == "date":
                from datetime import datetime
                value = datetime.strptime(value, "%Y-%m-%d").date()
            update_data_dict[key] = value

    # Handle image deletion field separately if sent
    if image_ids_to_delete:
        update_data_dict["image_ids_to_delete"] = json.loads(image_ids_to_delete)

    update_data = RoomUpdate(**update_data_dict)

    room = room_crud.update_room(db, room_id, update_data)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Delete selected images
    if update_data.image_ids_to_delete:
        for image_id in update_data.image_ids_to_delete:
            img = db.query(Image).filter(Image.id == image_id, Image.entity_id == room_id).first()
            if img and os.path.exists(img.image_url):
                os.remove(img.image_url)
                db.delete(img)
        db.commit()

    # Upload new images if sent
    UPLOAD_DIR = "uploads/rooms"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    if images:
        for image in images:
            ext = image.filename.split(".")[-1]
            file_name = f"{uuid.uuid4().hex}.{ext}"
            file_path = os.path.join(UPLOAD_DIR, file_name)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

            db.add(Image(entity_id=room.id, image_url=file_path))

    db.commit()
    room.images = db.query(Image).filter(Image.entity_id == room.id).all()

    return room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(room_id: int, db: Session = Depends(get_db)):
    deleted = room_crud.delete_room(db, room_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Room not found")
    


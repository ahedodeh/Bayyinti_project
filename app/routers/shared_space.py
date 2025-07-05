from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from typing import List, Optional
import os, uuid, shutil, json

from app.database import get_db
from app.schemas.shared_space import SharedSpaceCreate, SharedSpaceResponse, SharedSpaceUpdate
from app.crud import shared_space as crud
from app.models.image import Image
from app.enum.shared_space_type_enum import SharedSpaceTypeEnum

router = APIRouter(prefix="/shared-spaces", tags=["Shared Spaces"])

UPLOAD_DIR = "uploads/shared_spaces"

@router.post("/", response_model=SharedSpaceResponse, status_code=status.HTTP_201_CREATED)
async def create_shared_space(
    room_type: SharedSpaceTypeEnum = Form(...),
    property_id: int = Form(...),
    description: Optional[str] = Form(None),
    images: Optional[List[UploadFile]] = File(default=None),
    db: Session = Depends(get_db)
):
    if images is None:
        images = []

    payload = SharedSpaceCreate(room_type=room_type, property_id=property_id, description=description)
    shared_space = crud.create_shared_space(db, payload)

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    for image in images:
        ext = image.filename.split(".")[-1]
        file_name = f"{uuid.uuid4().hex}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_record = Image(entity_id=shared_space.id, entity_type="shared_space", image_url=file_path)
        db.add(image_record)

    db.commit()

    shared_space.images = db.query(Image).filter(
        Image.entity_id == shared_space.id,
        Image.entity_type == "shared_space"
    ).all()

    return shared_space


@router.get("/{id}", response_model=SharedSpaceResponse)
def get_shared_space(id: int, db: Session = Depends(get_db)):
    shared_space = crud.get_shared_space_by_id(db, id)
    if not shared_space:
        raise HTTPException(status_code=404, detail="Shared space not found")

    shared_space.images = db.query(Image).filter(
        Image.entity_id == shared_space.id,
        Image.entity_type == "shared_space"
    ).all()

    return shared_space


@router.get("/property/{property_id}", response_model=List[SharedSpaceResponse])
def get_shared_spaces_by_property(property_id: int, db: Session = Depends(get_db)):
    shared_spaces = crud.get_shared_spaces_by_property(db, property_id)
    for ss in shared_spaces:
        ss.images = db.query(Image).filter(
            Image.entity_id == ss.id,
            Image.entity_type == "shared_space"
        ).all()
    return shared_spaces


@router.put("/{id}", response_model=SharedSpaceResponse)
async def update_shared_space(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    images: Optional[List[UploadFile]] = File(default=None),
    image_ids_to_delete: Optional[str] = Form(None),
):
    if images is None:
        images = []

    form = await request.form()
    update_data = {}

    for key in SharedSpaceUpdate.__annotations__:
        if key in form and form[key] != "":
            val = form[key]
            if key == "room_type":
                val = SharedSpaceTypeEnum(val)

            update_data[key] = val

    if image_ids_to_delete:
        update_data["image_ids_to_delete"] = json.loads(image_ids_to_delete)

    update_payload = SharedSpaceUpdate(**update_data)

    shared_space = crud.update_shared_space(db, id, update_payload)
    if not shared_space:
        raise HTTPException(status_code=404, detail="Shared space not found")

    if update_payload.image_ids_to_delete:
        for image_id in update_payload.image_ids_to_delete:
            img = db.query(Image).filter(Image.id == image_id, Image.entity_id == id).first()
            if img and os.path.exists(img.image_url):
                os.remove(img.image_url)
                db.delete(img)
        db.commit()

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    for image in images:
        ext = image.filename.split(".")[-1]
        file_name = f"{uuid.uuid4().hex}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        db.add(Image(entity_id=shared_space.id, entity_type="shared_space", image_url=file_path))

    db.commit()

    shared_space.images = db.query(Image).filter(
        Image.entity_id == shared_space.id,
        Image.entity_type == "shared_space"
    ).all()

    return shared_space


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shared_space(id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_shared_space(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Shared space not found")
    return None

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.property_listing import PropertyListingCreate, PropertyListingUpdate, PropertyListingResponse
from app.crud import property_listing as crud
from app.enum.city import CityEnum
from app.enum.country import CountryEnum
import shutil, os
from uuid import uuid4

router = APIRouter(prefix="/property-listings", tags=["Property Listings"])

UPLOAD_DIR = "static/property_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_image_file(image: UploadFile) -> str:
    file_ext = image.filename.split(".")[-1]
    filename = f"{uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return f"/{file_path}"

@router.post("/", response_model=PropertyListingResponse, status_code=status.HTTP_201_CREATED)
async def create(
    landlord_id: str = Form(...),
    building_name: str = Form(None),
    building_number: str = Form(None),
    title: str = Form(None),
    description: str = Form(None),
    floor_number: int = Form(None),
    location_lat: str = Form(None),
    location_lon: str = Form(None),
    is_active: bool = Form(True),
    gender_preference: str = Form(None),
    has_gas: bool = Form(False),
    has_electricity: bool = Form(False),
    has_water: bool = Form(False),
    has_internet: bool = Form(False),
    property_type: str = Form(None),
    city: CityEnum = Form(None),
    country: CountryEnum = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    image_url = save_image_file(image) if image else None

    data = PropertyListingCreate(
        landlord_id=landlord_id,
        building_name=building_name,
        building_number=building_number,
        title=title,
        description=description,
        floor_number=floor_number,
        location_lat=location_lat,
        location_lon=location_lon,
        is_active=is_active,
        gender_preference=gender_preference,
        has_gas=has_gas,
        has_electricity=has_electricity,
        has_water=has_water,
        has_internet=has_internet,
        property_type=property_type,
        city=city,
        country=country,
        property_image=image_url,
    )
    return crud.create_property_listing(db, data)

@router.put("/{id}", response_model=PropertyListingResponse)
async def partial_update(
    id: int,
    landlord_id: str = Form(None),
    building_name: str = Form(None),
    building_number: str = Form(None),
    title: str = Form(None),
    description: str = Form(None),
    floor_number: int = Form(None),
    location_lat: str = Form(None),
    location_lon: str = Form(None),
    is_active: bool = Form(None),
    gender_preference: str = Form(None),
    has_gas: bool = Form(None),
    has_electricity: bool = Form(None),
    has_water: bool = Form(None),
    has_internet: bool = Form(None),
    property_type: str = Form(None),
    city: CityEnum = Form(None),
    country: CountryEnum = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    image_url = save_image_file(image) if image else None

    data = PropertyListingUpdate(
        landlord_id=landlord_id,
        building_name=building_name,
        building_number=building_number,
        title=title,
        description=description,
        floor_number=floor_number,
        location_lat=location_lat,
        location_lon=location_lon,
        is_active=is_active,
        gender_preference=gender_preference,
        has_gas=has_gas,
        has_electricity=has_electricity,
        has_water=has_water,
        has_internet=has_internet,
        property_type=property_type,
        city=city,
        country=country,
        property_image=image_url,
    )

    listing = crud.update_listing(db, id, data)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@router.get("/{id}", response_model=PropertyListingResponse)
def read_by_id(id: int, db: Session = Depends(get_db)):
    listing = crud.get_listing_by_id(db, id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@router.get("/landlord/{landlord_id}", response_model=list[PropertyListingResponse])
def read_by_landlord(landlord_id: str, db: Session = Depends(get_db)):
    return crud.get_listings_by_landlord(db, landlord_id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    listing = crud.delete_listing(db, id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return

@router.get("/", response_model=list[PropertyListingResponse])
def read_all(db: Session = Depends(get_db)):
    return crud.get_all_listings(db)

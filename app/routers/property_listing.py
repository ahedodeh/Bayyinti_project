from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.property_listing import PropertyListingCreate, PropertyListingResponse
from app.crud import property_listing as crud

router = APIRouter(prefix="/property-listings", tags=["Property Listings"])

@router.post("/", response_model=PropertyListingResponse, status_code=status.HTTP_201_CREATED)
def create(payload: PropertyListingCreate, db: Session = Depends(get_db)):
    return crud.create_property_listing(db, payload)

@router.get("/{id}", response_model=PropertyListingResponse)
def read_by_id(id: int, db: Session = Depends(get_db)):
    listing = crud.get_listing_by_id(db, id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@router.get("/landlord/{landlord_id}", response_model=list[PropertyListingResponse])
def read_by_landlord(landlord_id: int, db: Session = Depends(get_db)):
    return crud.get_listings_by_landlord(db, landlord_id)

@router.put("/{id}", response_model=PropertyListingResponse)
def update(id: int, payload: PropertyListingCreate, db: Session = Depends(get_db)):
    listing = crud.update_listing(db, id, payload)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    listing = crud.delete_listing(db, id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return

@router.get("/", response_model=list[PropertyListingResponse])
def read_all(db: Session = Depends(get_db)):
    return crud.get_all_listings(db)

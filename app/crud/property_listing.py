from sqlalchemy.orm import Session
from app.models.property_listing import PropertyListing
from app.schemas.property_listing import PropertyListingCreate

def create_property_listing(db: Session, data: PropertyListingCreate):
    listing = PropertyListing(**data.dict())
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing

def get_listing_by_id(db: Session, listing_id: int):
    return db.query(PropertyListing).filter(PropertyListing.id == listing_id).first()

def get_listings_by_landlord(db: Session, landlord_id: int):
    return db.query(PropertyListing).filter(PropertyListing.landlord_id == landlord_id).all()

def update_listing(db: Session, listing_id: int, data: PropertyListingCreate):
    listing = db.query(PropertyListing).filter(PropertyListing.id == listing_id).first()
    if listing:
        for key, value in data.dict().items():
            setattr(listing, key, value)
        db.commit()
        db.refresh(listing)
    return listing

def delete_listing(db: Session, listing_id: int):
    listing = db.query(PropertyListing).filter(PropertyListing.id == listing_id).first()
    if listing:
        db.delete(listing)
        db.commit()
    return listing

def get_all_listings(db: Session):
    return db.query(PropertyListing).all()

def get_all_listings(db: Session):
    listings = db.query(PropertyListing).all()
    for listing in listings:
        listing.number_of_rooms = len(listing.rooms) 
    return listings


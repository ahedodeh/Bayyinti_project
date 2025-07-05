from sqlalchemy.orm import Session, joinedload
from app.models.property_listing import PropertyListing
from app.schemas.property_listing import PropertyListingCreate, PropertyListingUpdate

def create_property_listing(db: Session, data: PropertyListingCreate):
    listing = PropertyListing(**data.dict())
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing

def get_listing_by_id(db: Session, listing_id: int):
    listing = db.query(PropertyListing).options(
        joinedload(PropertyListing.rooms),
        joinedload(PropertyListing.shared_spaces)
    ).filter(PropertyListing.id == listing_id).first()
    if listing:
        listing.number_of_rooms = len(listing.rooms) if listing.rooms else 0
    return listing

def get_listings_by_landlord(db: Session, landlord_id: str):
    listings = db.query(PropertyListing).options(
        joinedload(PropertyListing.rooms),
        joinedload(PropertyListing.shared_spaces)
    ).filter(PropertyListing.landlord_id == landlord_id).all()
    for listing in listings:
        listing.number_of_rooms = len(listing.rooms) if listing.rooms else 0
    return listings

def update_listing(db: Session, listing_id: int, data: PropertyListingUpdate):
    listing = db.query(PropertyListing).filter(PropertyListing.id == listing_id).first()
    if not listing:
        return None

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(listing, key, value)

    db.commit()
    db.refresh(listing)
    
    listing.number_of_rooms = len(listing.rooms) if listing.rooms else 0
    return listing

def delete_listing(db: Session, listing_id: int):
    listing = db.query(PropertyListing).filter(PropertyListing.id == listing_id).first()
    if listing:
        db.delete(listing)
        db.commit()
    return listing

def get_all_listings(db: Session):
    listings = db.query(PropertyListing).options(
        joinedload(PropertyListing.rooms),
        joinedload(PropertyListing.shared_spaces)
    ).all()
    for listing in listings:
        listing.number_of_rooms = len(listing.rooms) if listing.rooms else 0
    return listings

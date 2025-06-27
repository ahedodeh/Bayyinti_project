from sqlalchemy import Column, Integer, String, Boolean, Float, Date, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
from app.enum.room_type_enum import RoomTypeEnum

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    property_listing_id = Column(Integer, ForeignKey("property_listings.id"), nullable=False)

    description = Column(String(255), nullable=True)
    price_of_bed_per_month = Column(Float, nullable=True)
    available_from = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)

    room_type = Column(Enum(RoomTypeEnum), nullable=True)
    number_of_beds = Column(Integer, nullable=True)
    number_of_available_beds = Column(Integer, nullable=True)

    has_internal_bathroom = Column(Boolean, default=False)
    has_internal_balcony = Column(Boolean, default=False)
    has_ac = Column(Boolean, default=False)
    has_office = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    property_listing = relationship("PropertyListing", back_populates="rooms")

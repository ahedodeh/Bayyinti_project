# models/room.py

from sqlalchemy import Column, Integer, String, Boolean, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.Enums.room_type_enum import RoomTypeEnum



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

    property_listing = relationship("PropertyListing", back_populates="rooms")
    
    images = relationship("RoomImage", back_populates="room", cascade="all, delete-orphan")


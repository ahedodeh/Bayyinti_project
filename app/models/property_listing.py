from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.database import Base

class PropertyListing(Base):
    __tablename__ = "property_listings"

    id = Column(Integer, primary_key=True, index=True)
    building_name = Column(String(255), nullable=True)
    building_number = Column(String(50), nullable=True)
    landlord_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    floor_number = Column(Integer, nullable=True)
    number_of_rooms = Column(Integer, nullable=True)
    location_lat = Column(Float, nullable=True)
    location_lon = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    gender_preference = Column(String(20), nullable=True)
    has_gas = Column(Boolean, default=False)
    has_electricity = Column(Boolean, default=False)
    has_water = Column(Boolean, default=False)
    has_internet = Column(Boolean, default=False)
    
    rooms = relationship("Room", back_populates="property_listing", cascade="all, delete-orphan")
    

from sqlalchemy import Column, Integer, String, Boolean, Enum as SqlEnum, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
from app.enums.city import CityEnum
from app.enums.country import CountryEnum


class PropertyListing(Base):
    __tablename__ = "property_listings"

    id = Column(Integer, primary_key=True, index=True)
    building_name = Column(String(255), nullable=True)
    building_number = Column(String(50), nullable=True)
    landlord_id = Column(String(255), nullable=False)
    title = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    floor_number = Column(Integer, nullable=True)
    number_of_rooms = Column(Integer, nullable=True)
    location_lat = Column(String(50), nullable=True)
    location_lon = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    gender_preference = Column(String(20), nullable=True)
    has_gas = Column(Boolean, default=False)
    has_electricity = Column(Boolean, default=False)
    has_water = Column(Boolean, default=False)
    has_internet = Column(Boolean, default=False)
    property_type = Column(String(100), nullable=True)
    property_image = Column(String(255), nullable=True)
    city = Column(SqlEnum(CityEnum), nullable=True)
    country = Column(SqlEnum(CountryEnum), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    rooms = relationship("Room", back_populates="property_listing", cascade="all, delete-orphan")
    shared_spaces = relationship("SharedSpace", back_populates="property_listing", cascade="all, delete-orphan")

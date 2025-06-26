from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SqlEnum, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
from app.enums.shared_space_type_enum import SharedSpaceTypeEnum

class SharedSpace(Base):
    __tablename__ = "shared_spaces"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    room_type = Column(SqlEnum(SharedSpaceTypeEnum), nullable=False)
    description = Column(String(255), nullable=True)

    property_id = Column(Integer, ForeignKey("property_listings.id"), nullable=False)
    property_listing = relationship("PropertyListing", backref="shared_spaces")

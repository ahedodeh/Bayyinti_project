from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255))
    landlord_id = Column(Integer, ForeignKey("landlords.id"), nullable=False)

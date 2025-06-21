from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    property_listing_id = Column(Integer, ForeignKey("property_listings.id"), nullable=False)

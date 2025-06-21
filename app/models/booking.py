from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    bed_id = Column(Integer, ForeignKey("beds.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

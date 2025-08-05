from sqlalchemy import Column, Integer, String, ForeignKey,Date, Enum as SqlEnum, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    college = Column(String)
    specialization = Column(String)
    university_campus = Column(String)
    date_of_birth = Column(Date)
    degree = Column(String)
    gender = Column(String)
    user_id = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # bookings = relationship("Booking", back_populates="student")

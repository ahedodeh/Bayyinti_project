from sqlalchemy import Column, Integer, String, Date
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

    # bookings = relationship("Booking", back_populates="student")

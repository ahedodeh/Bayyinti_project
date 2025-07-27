from enum import Enum

class CollegeEnum(str, Enum):
    engineering = "Engineering"
    science = "Science"
    arts = "Arts"
    medicine = "Medicine"

class DegreeEnum(str, Enum):
    bs = "BS"
    master = "Master"
    dr = "Dr"

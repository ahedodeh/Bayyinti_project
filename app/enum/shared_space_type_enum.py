from enum import Enum

class SharedSpaceTypeEnum(str, Enum):
    kitchen = "Kitchen"
    living_room = "Living Room"
    laundry = "Laundry"
    gym = "Gym"
    other = "Others"

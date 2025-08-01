from enum import Enum

class UserRole(str, Enum):
    STD = "Std"
    LR = "LR"
    ADMIN = "Admin"

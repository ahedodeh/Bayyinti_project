from pydantic import BaseModel

class BookmarkBase(BaseModel):
    student_id: int
    property_listing_id: int

class BookmarkCreate(BookmarkBase):
    pass

class BookmarkOut(BookmarkBase):
    id: int

    class Config:
        orm_mode = True

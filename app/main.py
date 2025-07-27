from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles 
import os

from app.database import Base, engine
from app import models
from app.routers import room_router, property_listing_router, image_router, shared_space_router, student_router

app = FastAPI()

app.mount("/static", StaticFiles(directory=os.path.join(os.getcwd(), "static")), name="static")
app.mount("/uploads", StaticFiles(directory=os.path.join(os.getcwd(), "uploads")), name="uploads")

Base.metadata.create_all(bind=engine)  

app.include_router(room_router)
app.include_router(property_listing_router)
app.include_router(image_router)
app.include_router(shared_space_router)
app.include_router(student_router)

@app.get("/")
def read_root():
    return {"message": "API is running"}

# uvicorn app.main:app --reload
#

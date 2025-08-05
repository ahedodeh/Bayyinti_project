from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware 

import os
from app.database import Base, engine
from app import models
from app.routers import room_router, property_listing_router, image_router, shared_space_router, student_router, user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

app.mount("/static", StaticFiles(directory=os.path.join(os.getcwd(), "static")), name="static")
app.mount("/uploads", StaticFiles(directory=os.path.join(os.getcwd(), "uploads")), name="uploads")

Base.metadata.create_all(bind=engine)

app.include_router(room_router)
app.include_router(property_listing_router)
app.include_router(image_router)
app.include_router(shared_space_router)
app.include_router(student_router)
app.include_router(user_router)

@app.get("/")
def read_root():
    return {"message": "API is running"}

# uvicorn app.main:app --reload

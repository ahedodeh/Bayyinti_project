from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import room_router, property_listing_router, image_router,shared_space_router

app = FastAPI()

Base.metadata.create_all(bind=engine)  

app.include_router(room_router)
app.include_router(property_listing_router)
app.include_router(image_router)
app.include_router(shared_space_router)

@app.get("/")
def read_root():
    return {"message": "API is running"}


# uvicorn app.main:app --reload
# alembic revision --autogenerate -m "add is_available column to rooms"
# alembic upgrade head

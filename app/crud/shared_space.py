from sqlalchemy.orm import Session
from app.models.shared_space import SharedSpace
from app.schemas.shared_space import SharedSpaceCreate, SharedSpaceUpdate

def create_shared_space(db: Session, data: SharedSpaceCreate):
    shared_space = SharedSpace(**data.dict())
    db.add(shared_space)
    db.commit()
    db.refresh(shared_space)
    return shared_space

def get_shared_space_by_id(db: Session, shared_space_id: int):
    return db.query(SharedSpace).filter(SharedSpace.id == shared_space_id).first()

def get_shared_spaces_by_property(db: Session, property_id: int):
    return db.query(SharedSpace).filter(SharedSpace.property_id == property_id).all()

def update_shared_space(db: Session, shared_space_id: int, updates: SharedSpaceUpdate):
    shared_space = db.query(SharedSpace).filter(SharedSpace.id == shared_space_id).first()
    if shared_space:
        for key, value in updates.dict(exclude_unset=True).items():
            setattr(shared_space, key, value)
        db.commit()
        db.refresh(shared_space)
    return shared_space

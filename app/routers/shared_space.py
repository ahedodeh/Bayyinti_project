from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.shared_space import SharedSpaceCreate, SharedSpaceResponse, SharedSpaceUpdate
from app.crud import shared_space as crud

router = APIRouter(prefix="/shared-spaces", tags=["Shared Spaces"])

@router.post("/", response_model=SharedSpaceResponse, status_code=status.HTTP_201_CREATED)
def create_shared_space(payload: SharedSpaceCreate, db: Session = Depends(get_db)):
    return crud.create_shared_space(db, payload)

@router.get("/{id}", response_model=SharedSpaceResponse)
def get_shared_space(id: int, db: Session = Depends(get_db)):
    shared_space = crud.get_shared_space_by_id(db, id)
    if not shared_space:
        raise HTTPException(status_code=404, detail="Shared space not found")
    return shared_space

@router.get("/property/{property_id}", response_model=list[SharedSpaceResponse])
def get_shared_spaces_by_property(property_id: int, db: Session = Depends(get_db)):
    return crud.get_shared_spaces_by_property(db, property_id)

@router.put("/{id}", response_model=SharedSpaceResponse, summary="Partial Update")
def partial_update_shared_space(id: int, payload: SharedSpaceUpdate, db: Session = Depends(get_db)):
    updated_shared_space = crud.update_shared_space(db, id, payload)
    if not updated_shared_space:
        raise HTTPException(status_code=404, detail="Shared space not found")
    return updated_shared_space


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shared_space(id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_shared_space(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Shared space not found")
    return None

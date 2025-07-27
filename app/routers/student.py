from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import app.crud.student as student_crud
import app.schemas.student as student_schema

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=student_schema.StudentOut)
def create_student(student: student_schema.StudentCreate, db: Session = Depends(get_db)):
    return student_crud.create_student(db, student)

@router.get("/", response_model=list[student_schema.StudentOut])
def get_students(db: Session = Depends(get_db)):
    return student_crud.get_students(db)

@router.get("/id/{student_id}", response_model=student_schema.StudentOut)
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = student_crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/user/{user_id}", response_model=student_schema.StudentOut)
def get_student_by_user_id(user_id: str, db: Session = Depends(get_db)):
    student = student_crud.get_student_by_user_id(db, user_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    result = student_crud.delete_student(db, student_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted"}

@router.put("/{student_id}", response_model=student_schema.StudentOut)
def partial_update_student(student_id: int, student_update: student_schema.StudentUpdate, db: Session = Depends(get_db)):
    student = student_crud.update_student_partial(db, student_id, student_update)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

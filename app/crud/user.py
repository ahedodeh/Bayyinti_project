# app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.UserId == user_id).first()

def get_users(db: Session, page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size
    return db.query(User).offset(skip).limit(page_size).all()

def get_users_with_count(db: Session, page: int = 1, page_size: int = 10):
    total = db.query(User).count()
    skip = (page - 1) * page_size
    users = db.query(User).offset(skip).limit(page_size).all()
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "users": users
    }


def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.Password) if user.Password else None
    db_user = User(
        Email=user.Email,
        Phone=user.Phone,
        FullName=user.FullName,
        Password=hashed_password,
        Role=user.Role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    update_data = user.dict(exclude_unset=True)

    if "Password" in update_data and update_data["Password"]:
        update_data["Password"] = pwd_context.hash(update_data["Password"])

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

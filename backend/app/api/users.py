from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/users/", response_model=schemas.user.UserRead)
def create_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    new_user = models.user.User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/", response_model=list[schemas.user.UserRead])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.user.User).all()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app import models, schemas

router = APIRouter()

@router.post("/users/", response_model=schemas.user.UserRead)
def create_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.user.User).filter(models.user.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    new_user = models.user.User(name=user.name, email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.user.User).filter(models.user.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/", response_model=list[schemas.user.UserRead])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.user.User).all()

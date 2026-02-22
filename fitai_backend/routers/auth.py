from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from database import db as db_models
from database.auth import hash_password, verify_password, create_access_token
from models.schemas import RegisterRequest, LoginRequest, TokenResponse, MessageResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=MessageResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    # Check if email already exists
    existing = db.query(db_models.User).filter(
        db_models.User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    user = db_models.User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": f"User {data.name} registered successfully!"}

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(
        db_models.User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    token = create_access_token({"user_id": user.id, "email": user.email})
    return {
        "access_token": token,
        "token_type":   "bearer",
        "user_id":      user.id,
        "name":         user.name,
    }

@router.get("/me")
def get_me():
    return {"message": "Use token to access protected routes"}

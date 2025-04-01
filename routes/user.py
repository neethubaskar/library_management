from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Book, MemberBook, User
from schemas import UserCreate, UserResponse
from database import get_db
from auth import hash_password, create_jwt_token, verify_password, get_current_user
import datetime

router = APIRouter()


@router.post("/register")
def  register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user with validation and role."""
    
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)
    # api_key = str(uuid.uuid4())

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        phone_number=user_data.phone_number,
        role=user_data.role,
        # api_key=api_key
    )

    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}


@router.post("/login")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token(user.id, user.role)
    return {"token": token}


@router.get("/profile")
def get_user_profile(current_user=Depends(get_current_user)):
    """Fetch the profile of the currently logged-in user."""
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }

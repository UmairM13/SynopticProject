from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.user_models import User
from pydantic import BaseModel
from typing import Optional
from datetime import date


router = APIRouter()


# Pydantic model for request validation
class UserCreate(BaseModel):
    nationality: Optional[str] = None
    current_city: Optional[str] = None
    current_country:  Optional[str] = nationality
    age:  Optional[int] = None
    preferred_climate:  Optional[str] = None
    preferred_terrain:  Optional[str] = None
    past_destinations:  Optional[str] = None
    budget:  Optional[float] = None
    holiday_type:  Optional[str] = None
    trip_start_date: Optional[date] = None
    trip_end_date: Optional[date] = None
    email: str
    password: str
    salt: Optional[str] = None
    session_token: Optional[str] = None


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/users")
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "nationality": new_user.nationality,
        "current_city": new_user.current_city,
        "current_country": new_user.current_country,
        "age": new_user.age,
        "preferred_climate": new_user.preferred_climate,
        "preferred_terrain": new_user.preferred_terrain,
        "past_destinations": new_user.past_destinations,
        "budget": new_user.budget,
        "holiday_type": new_user.holiday_type,
        "trip_start_date": new_user.trip_start_date,
        "trip_end_date": new_user.trip_end_date,
        "email": new_user.email
        # Not returning password and salt for security reasons
    }

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "nationality": user.nationality,
        "current_city": user.current_city,
        "current_country": user.current_country,
        "age": user.age,
        "preferred_climate": user.preferred_climate,
        "preferred_terrain": user.preferred_terrain,
        "past_destinations": user.past_destinations,
        "budget": user.budget,
        "holiday_type": user.holiday_type,
        "trip_start_date": user.trip_start_date,
        "trip_end_date": user.trip_end_date,
        "email": user.email
    }
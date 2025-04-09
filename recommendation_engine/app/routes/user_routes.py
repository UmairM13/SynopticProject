from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.user_models import User


router = APIRouter()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/users")
def create_user(user_data: dict, db: Session = Depends(get_db)):
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "nationality": new_user.nationality,
        "current_city": new_user.current_city,
        "current_country": new_user.current_country,
        "age": new_user.age,
        "preferred_destination": new_user.preferred_destination,
        "past_destinations": new_user.past_destinations,
        "budget": new_user.budget,
        "holiday_type": new_user.holiday_type
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
        "preferred_destination": user.preferred_destination,
        "past_destinations": user.past_destinations,
        "budget": user.budget,
        "holiday_type": user.holiday_type
    }
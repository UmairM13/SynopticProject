from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
from recommendation_engine.api.models.database import SessionLocal
from recommendation_engine.api.models.user_models import User
from recommendation_engine.api.controllers import user_controllers as user_service
from recommendation_engine.api.utils.auth import require_authentication


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
async def create_user(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"{field} is required")
    
    db_user = user_service.create_user(db, data)
    return {
        "id": db_user.id,
        "email": db_user.email,
        "message": "User created successfully"
    }


@router.get("/me")
def get_current_user(db: Session = Depends(get_db),
                     X_Authorization: str = Header(None)):
    
    if not X_Authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    user = user_service.get_user_by_token(db, X_Authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session token")
    
    return {
        "id": user.id,
        "email": user.email,
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
        "created_at": user.created_at
    }


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "email": user.email,
        "nationality": user.nationality,
        "preferred_climate": user.preferred_climate,
        "preferred_terrain": user.preferred_terrain,
        "budget": user.budget,
        "current_city": user.current_city,
        "current_country": user.current_country,
        "trip_start_date": user.trip_start_date,
        "trip_end_date": user.trip_end_date,
        "past_destinations": user.past_destinations,
    }

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    user = user_service.authenticate_user(db, data['email'], data['password'])
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "id": user.id,
        "session_token": user.session_token,
        "has_onboarded": user.has_onboarded,
        "message": "Login successful"
    }
    

@router.post("/logout")
async def logout(db: Session = Depends(get_db), 
                 session_token: str = Header(..., alias="X-Authorization")):
    
    user = db.query(User).filter(User.session_token == session_token).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session token")
    
    user_service.logout_user(db, user.id)
    return {"message": "Logout successful"}


@router.patch("/{user_id}")
def update_user(user_id: int, user_update: dict, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if "past_destinations" in user_update:
        existing = user.past_destinations.split(",") if user.past_destinations else []
        new = [d.strip() for d in user_update["past_destinations"].split(",")]
        merged = list(set(existing + new))
        user.past_destinations = ",".join(merged)
        user_update.pop("past_destinations")

    for key, value in user_update.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/")
def delete_user(
    current_user: User = Depends(require_authentication()),
    db: Session = Depends(get_db)):
    
    user_service.delete_user(db, current_user.id)
    return {"message": "User deleted successfully"}


@router.post("/{user_id}/past-destinations")
def add_destination(user_id: int, data: dict, db: Session = Depends(get_db)):
    return user_service.add_past_destination(db, user_id, data)

@router.get("/{user_id}/past-destinations")
def get_user_past_destinations(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_past_destinations(db, user_id)

@router.patch("/{user_id}/past-destinations/{destination_id}")
def update_past_destination(user_id: int, destination_id: int, data: dict, db: Session = Depends(get_db)):
    updated = user_service.update_past_destination(db, user_id, destination_id, data)
    if isinstance(updated, dict) and updated.get("error"):
        raise HTTPException(status_code=404, detail=updated["error"])
    return updated

@router.delete("/{user_id}/past-destinations/{destination_id}")
def delete_past_destination(user_id: int, destination_id: int, db: Session = Depends(get_db)):
    deleted = user_service.delete_past_destination(db, user_id, destination_id)
    if isinstance(deleted, dict) and deleted.get("error"):
        raise HTTPException(status_code=404, detail=deleted["error"])
    return {"message": "Past destination deleted successfully"}


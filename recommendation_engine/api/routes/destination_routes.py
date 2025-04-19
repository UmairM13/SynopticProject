from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
from recommendation_engine.api.models.database import SessionLocal
from recommendation_engine.api.models.user_models import User
from recommendation_engine.api.controllers import destination_controllers as destination_service


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@router.get("/")
def get_all_destinations(db: Session = Depends(get_db)):
    destinations = destination_service.get_all_destinations(db)
    if not destinations:
        raise HTTPException(status_code=404, detail="No destinations found")
   
    return {
        "destinations": [
            {
                "id": destination.id,
                "name": destination.name,
                "country": destination.country,
                "off_season_start": destination.off_season_start,
                "off_season_end": destination.off_season_end,
                "climate": destination.climate,
                "terrain": destination.terrain,
                "avg_daily_budget": destination.avg_daily_budget,
                "currency": destination.currency,
                "language": destination.language,
                "safety_rating": destination.safety_rating,
            } for destination in destinations
        ]
    }


@router.get("/{destination_id}")
def get_user(destination_id: int, db: Session = Depends(get_db)):
    destination = destination_service.get_destination(db, destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    return {
        "id": destination.id,
            "name": destination.name,
            "country": destination.country,
            "off_season_start": destination.off_season_start,
            "off_season_end": destination.off_season_end,
            "climate": destination.climate,
            "terrain": destination.terrain,
            "avg_daily_budget": destination.avg_daily_budget,
            "currency": destination.currency,
            "language": destination.language,
            "safety_rating": destination.safety_rating,
    }
import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
import pandas as pd
from recommendation_engine.api.models.database import SessionLocal
from recommendation_engine.api.models.destination_models import Destination
from recommendation_engine.api.models.user_models import User
from recommendation_engine.api.models.recommendation_models import UserRecommendation


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@router.get("/top-destinations")
def top_destinations(db: Session = Depends(get_db)):
    results = (
        db.query(UserRecommendation.destination_name, func.count(UserRecommendation.destination_name).label("count"))
        .group_by(UserRecommendation.destination_name)
        .order_by(func.count(UserRecommendation.destination_name).desc())
        .limit(10)
        .all()
    )
    return [{
        "destination_name": r[0],
        "count": r[1]
    } for r in results]
    

@router.get("/user-stats")
def user_stats(db: Session = Depends(get_db)):
    total_users = db.query(func.count(User.id)).scalar()
    avg_age = db.query(func.avg(User.age)).scalar()
    avg_budget = db.query(func.avg(User.budget)).scalar()
    avg_trip_duration = (
        db.query(
            func.avg(func.datediff(User.trip_end_date, User.trip_start_date))
        )
        .filter(User.trip_start_date.isnot(None), User.trip_end_date.isnot(None))
        .scalar()
    )
    top_climate = db.query(User.preferred_climate, func.count(User.id)).group_by(User.preferred_climate).order_by(func.count(User.id).desc()).first()
    top_terrain = db.query(User.preferred_terrain, func.count(User.id)).group_by(User.preferred_terrain).order_by(func.count(User.id).desc()).first()
    top_holiday_type = db.query(User.holiday_type, func.count(User.id)).group_by(User.holiday_type).order_by(func.count(User.id).desc()).first()
    top_nationalities = db.query(User.nationality, func.count()).group_by(User.nationality).order_by(func.count().desc()).limit(5).all()
    total_recommendations = db.query(func.count(UserRecommendation.id)).scalar()
    
    return {
        "total_users": total_users,
        "avg_age": avg_age,
        "avg_budget": avg_budget,
        "avg_trip_duration": avg_trip_duration,
        "top_climate": top_climate[0] if top_climate else None,
        "top_terrain": top_terrain[0] if top_terrain else None,
        "top_holiday_type": top_holiday_type[0] if top_holiday_type else None,
        "top_nationalities": [{"country": country, "count": count} for country, count in top_nationalities],
        "total_recommendations": total_recommendations
    }
    

@router.get("/recommendation-activity")
def recommendation_activity(db: Session = Depends(get_db)):
    results = (
        db.query(
            extract("year", UserRecommendation.created_at).label("year"),
            extract("month", UserRecommendation.created_at).label("month"),
            func.count(UserRecommendation.id)
        )
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )
    
    return [
        {
            "year": r[0],
            "month": r[1],
            "count": r[2]
        } for r in results
    ]
    
    
@router.get("/preferences-distribution")
def preference_distribution(db: Session = Depends(get_db)):
    
    climates = db.query(User.preferred_climate, func.count(User.id)).group_by(User.preferred_climate).all()
    terrains = db.query(User.preferred_terrain, func.count(User.id)).group_by(User.preferred_terrain).all()
    
    return {
        "climates": [{"climate": r[0], "count": r[1]} for r in climates],
        "terrains": [{"terrain": r[0], "count": r[1]} for r in terrains]
    }
    

@router.get("/past-destinations-by-age")
def past_destination_by_age(db: Session = Depends(get_db)):
    
    users = db.query(User.age, User.past_destinations).filter(User.past_destinations.isnot(None)).all()
    records = []
    
    for age, destinations in users:
        if not destinations:
            continue
        for dest in destinations.split(","):
            records.append({
                "age": age,
                "destination": dest.strip()
            })
    
    df = pd.DataFrame(records)
    result = df.groupby(['age', 'destination']).size().reset_index(name='count')
    
    return result.to_dict(orient="records")


@router.get("/past-destinations-by-nationality")
def past_destinations_by_nationality(db: Session = Depends(get_db)):
    
    users = db.query(User.nationality, User.past_destinations).filter(User.past_destinations.isnot(None)).all()
    records = []
    
    for nationality, destinations in users:
        if not destinations:
            continue
        for dest in destinations.split(","):
            records.append({
                "nationality": nationality,
                "destination": dest.strip()
            })
        
    df = pd.DataFrame(records)
    result = df.groupby(['nationality', 'destination']).size().reset_index(name='count')
    
    return result.to_dict(orient="records")


@router.get("/off-season-rate")
def off_season_recommendation_rate(db: Session = Depends(get_db)):
    
    current_month = datetime.datetime.now().month
    
    total_recommendations = db.query(UserRecommendation).count()
    
    if total_recommendations == 0:
        return {
            "off_season_recommendations": 0,
            "peak_season_recommendations": 0,
            "off_season_ratio": "0%"
        }
    
    off_season_count = (
        db.query(UserRecommendation) .join(Destination, Destination.id == UserRecommendation.destination_id)
        .filter(
            Destination.off_season_start.isnot(None),
            Destination.off_season_end.isnot(None)
        )
        .filter(
            ((Destination.off_season_start <= Destination.off_season_end) &
             (current_month >= Destination.off_season_start) &
             (current_month <= Destination.off_season_end))
            |
            ((Destination.off_season_start > Destination.off_season_end) &
             ((current_month >= Destination.off_season_start) |
              (current_month <= Destination.off_season_end)))
        )
        .count()
    )
    
    peak_season_count = total_recommendations - off_season_count
    
    ratio = f"{round((off_season_count / total_recommendations) * 100, 2)}%"
    
    return{
        "off_season_recommendations": off_season_count,
        "peak_season_recommendations": peak_season_count,
        "off_season_ratio": ratio
    }

@router.get("/off-season-monthly")
def off_season_monthly_recommendations(db: Session = Depends(get_db)):
    import calendar

    # Map month names to numbers
    month_name_to_num = {month: i for i, month in enumerate(calendar.month_name) if month}
    months = list(calendar.month_name)[1:]  # ['January', ..., 'December']

    distribution = []

    all_destinations = db.query(Destination).filter(
        Destination.off_season_start.isnot(None),
        Destination.off_season_end.isnot(None)
    ).all()

    for i, month in enumerate(months, start=1):
        count = 0
        for dest in all_destinations:
            start = month_name_to_num.get(str(dest.off_season_start), None)
            end = month_name_to_num.get(str(dest.off_season_end), None)

            if start is None or end is None:
                continue

            if start <= end:
                if start <= i <= end:
                    count += 1
            else:  # Wrap-around (e.g. November to February)
                if i >= start or i <= end:
                    count += 1

        distribution.append({
            "month": month,
            "off_season_destinations": count
        })

    return distribution
    


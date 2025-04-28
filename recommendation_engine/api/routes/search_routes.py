from fastapi import APIRouter, Depends, HTTPException, Query
from recommendation_engine.api.models.database import SessionLocal
from recommendation_engine.recommender.content_based_model import prepare_features, recommend_similar_destinations
from recommendation_engine.recommender.data_loader import load_processed_data
from recommendation_engine.recommender.data_loader import DataManager
from recommendation_engine.api.models.destination_models import Destination
from sqlalchemy import or_
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
data_manager = DataManager.get_instance()
destinations_df = data_manager.get_destinations()

# Load and prepare once at startup
_, destinations_df, _ = load_processed_data()
features_df, similarity_matrix = prepare_features(destinations_df)

@router.get("/search-similar")
async def search_similar(destination_name: str = Query(..., description="Destination name to search similar places for")):
    destination_name = destination_name.strip()

    try:
        recommendations = recommend_similar_destinations(destination_name, destinations_df, features_df, similarity_matrix, top_n=10)
        if isinstance(recommendations, str):  # If an error string returned
            raise HTTPException(status_code=404, detail=recommendations)
        
        # Clean result
        return recommendations.to_dict(orient="records")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to find similar destinations. {str(e)}")


@router.get("/popular-destinations")
async def get_popular_destinations():
    # Hardcoded popular destinations for now
    popular_names = ["London", "Paris", "New York", "Tokyo", "Sydney", "Rome", "Dubai", "Bangkok", "Barcelona", "Cape Town"]
    
    popular_destinations = destinations_df[destinations_df['name'].isin(popular_names)][['id', 'name']]
    return popular_destinations.to_dict(orient="records")



@router.get("/search")
def search_destinations(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    query = query.lower().strip()

    matches = db.query(Destination).filter(
        or_(
            Destination.name.ilike(f"%{query}%"),
            Destination.country.ilike(f"%{query}%"),
            Destination.terrain.ilike(f"%{query}%"),
            Destination.climate.ilike(f"%{query}%"),
            Destination.holiday_type.ilike(f"%{query}%")
        )
    ).all()

    results = [
        {
            "id": dest.id,
            "name": dest.name,
            "country": dest.country,
            "avg_daily_budget": dest.avg_daily_budget,
        }
        for dest in matches
    ]

    return {"results": results}
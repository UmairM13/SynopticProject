from fastapi import HTTPException
from recommendation_engine.recommender.hybrid_recommender import recommend_destinations as hybrid_recommend, explain_recommendation
from recommendation_engine.api.models.recommendation_models import UserRecommendation
from sqlalchemy.orm import Session
from recommendation_engine.recommender.data_loader import DataManager


def get_recommendations_for_user(user_id: int):
    data_manager = DataManager.get_instance()
    users_df = data_manager.get_users()
    destinations_df = data_manager.get_destinations()
    past_destinations_df = data_manager.get_past_destinations()

    # Pass properly cleaned DataFrames into hybrid_recommend
    return hybrid_recommend(user_id, users_df, destinations_df, past_destinations_df)


def get_explanation_for_destination(user_id: int, destination_id: int):
    data_manager = DataManager.get_instance()
    data_manager.refresh()
    
    users_df = data_manager.get_users()
    destinations_df = data_manager.get_destinations()
    past_destinations_df = data_manager.get_past_destinations()
    
    return explain_recommendation(destination_id, user_id, users_df, destinations_df, past_destinations_df)


def save_recommendations(db: Session, user_id: int, destination_id: int, name: str, explanation: str = ""):
    existing = db.query(UserRecommendation).filter_by(user_id=user_id, destination_id=destination_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Recommendation already saved.")

    recommendation = UserRecommendation(
        user_id=user_id,
        destination_id=destination_id,
        destination_name=name,
        explanation=explanation
    )
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    return recommendation


def get_user_recommendations(db: Session, user_id: int):
    return db.query(UserRecommendation).filter(UserRecommendation.user_id == user_id).all()
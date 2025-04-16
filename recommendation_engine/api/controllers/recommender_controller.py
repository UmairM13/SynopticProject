from recommendation_engine.recommender.hybrid_recommender import recommend_destinations as hybrid_recommend, explain_recommendation
from recommendation_engine.api.models.recommendation_models import UserRecommendation
from sqlalchemy.orm import Session


def get_recommendations_for_user(user_id: int):
    return hybrid_recommend(user_id)

def get_explanation_for_destination(user_id:int, destination_name:int):
    return explain_recommendation(destination_name, user_id)

def save_recommendations(db: Session, user_id: int, destination_id: int, name: str, explanation: str=""):
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
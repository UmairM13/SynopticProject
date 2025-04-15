from fastapi import APIRouter, HTTPException
from recommendation_engine.api.models.recommendation_model import RecommendationRequest
from recommendation_engine.api.controllers.recommender_controller import get_recommendations_for_user, get_explanation_for_destination


router = APIRouter()


@router.post("/recommendations")
def recommend_destinations(req: RecommendationRequest):
    results = get_recommendations_for_user(req.user_id, req.top_n)
    if isinstance(results, str):
        raise HTTPException(status_code=404, detail=results)
    return results.to_dict(orient="records")

@router.get("/explanation/{user_id}/destination_name")
def explain_destination(user_id: int, destination_name: str):
    explanation = get_explanation_for_destination(user_id, destination_name)
    if isinstance(explanation, str):
        raise HTTPException(status_code=404, detail=explanation)
    return {"destination": destination_name, "explanation": explanation}

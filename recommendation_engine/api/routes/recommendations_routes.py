from fastapi import APIRouter, HTTPException
from recommendation_engine.api.controllers.recommender_controller import get_recommendations_for_user, get_explanation_for_destination
from recommendation_engine.recommender.data_preprocessing import run_preprocessing


router = APIRouter()


@router.get("/{user_id}")
def recommend_destinations(user_id: int):
    results = get_recommendations_for_user(user_id)
    if isinstance(results, str):
        raise HTTPException(status_code=404, detail=results)
    return results.to_dict(orient="records")

@router.get("/explanation/{user_id}/{destination_name}")
def explain_destination(user_id: int, destination_name: int):
    explanation = get_explanation_for_destination(user_id, destination_name)
    if isinstance(explanation, int):
        raise HTTPException(status_code=404, detail=explanation)
    return {"destination": destination_name, "explanation": explanation}

@router.post("/preprocess")
def preprocess_data():
    result = run_preprocessing()
    return result
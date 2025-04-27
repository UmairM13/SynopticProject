from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from recommendation_engine.api.models.user_models import User
from recommendation_engine.api.controllers import recommender_controller as controller
from recommendation_engine.api.models.database import SessionLocal
from recommendation_engine.recommender.data_preprocessing import run_preprocessing
from recommendation_engine.api.utils.auth import require_authentication

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/saved")
def get_saved_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authentication())):
    
    saved_recommendations = controller.get_user_recommendations(db, current_user.id)
    
    return [{
        "destination_id": rec.destination_id,
        "destination": rec.destination_name,
        "explanation": rec.explanation,
        "timestamp": rec.created_at
    } for rec in saved_recommendations]

    
@router.get("/{user_id}")
def recommend_destinations(user_id: int):
    results = controller.get_recommendations_for_user(user_id)
    if isinstance(results, str):
        raise HTTPException(status_code=404, detail=results)
    return results.to_dict(orient="records")

@router.get("/explanation/{user_id}/{destination_name}")
def explain_destination(user_id: int, destination_name: int):
    explanation = controller.get_explanation_for_destination(user_id, destination_name)
    if isinstance(explanation, int):
        raise HTTPException(status_code=404, detail=explanation)
    return {"destination": destination_name, "explanation": explanation}

@router.post("/preprocess")
def preprocess_data():
    result = run_preprocessing()
    return result


@router.post("/save")
async def save_recommendation(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authentication())
):
    data = await request.json()
    destination_id = data.get("destination_id")
    destination_name = data.get("destination_name")
    explanation = data.get("explanation", "")
    
    if not destination_id or not destination_name:
        raise HTTPException(status_code=400, detail="destination_id and destination_name are required")
    
    try:
        saved = controller.save_recommendations(db, current_user.id, destination_id, destination_name, explanation)
    except HTTPException as e:
        # If already saved, bubble up the error
        raise e

    return {
        "message": "Recommendation saved successfully",
        "destination": saved.destination_name,
        "timestamp": saved.created_at
    }
    

@router.delete("/save/{destination_id}")
async def delete_saved_recommendation(
    destination_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_authentication())
):
    saved_recommendations = controller.get_user_recommendations(db, current_user.id)

    if not saved_recommendations:
        raise HTTPException(status_code=404, detail="No saved recommendations found")

    for rec in saved_recommendations:
        if rec.destination_id == destination_id:
            db.delete(rec)
            db.commit()
            return {"message": "Recommendation deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Recommendation not found")
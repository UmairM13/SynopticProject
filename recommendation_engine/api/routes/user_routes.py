from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
from recommendation_engine.api.models.database import SessionLocal
from recommendation_engine.api.models.user_models import User
from recommendation_engine.api.controllers import user_controllers as user_service

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
        "budget": user.budget
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
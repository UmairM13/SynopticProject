from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from recommendation_engine.api.models.database import SessionLocal
from recommendation_engine.api.controllers import user_controllers

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_authentication():
    def wrapper(X_Authorization: str = Header(None), db: Session = Depends(get_db)):
        if not X_Authorization:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        user = user_controllers.get_user_by_token(db, X_Authorization)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid session token")
        return user
    return wrapper


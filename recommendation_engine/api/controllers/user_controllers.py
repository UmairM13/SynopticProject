from sqlalchemy.orm import Session
from recommendation_engine.api.models.user_models import User
from recommendation_engine.api.models.past_destination_model import PastDestination
import uuid, hashlib, os

def create_user(db: Session, user_data: dict):
    salt = uuid.uuid4().hex
    hashed_pw = hashlib.sha256((user_data['password'] + salt).encode()).hexdigest()
    
    db_user = User(
        email=user_data['email'],
        password=hashed_pw,
        salt=salt,
        nationality=user_data['nationality'],
        current_city=user_data['current_city'],
        current_country=user_data['current_country'],
        age=user_data['age'],
        preferred_climate=user_data['preferred_climate'],
        preferred_terrain=user_data['preferred_terrain'],
        past_destinations=user_data['past_destinations'],
        budget=user_data['budget'],
        holiday_type=user_data['holiday_type'],
        trip_start_date=user_data['trip_start_date'],
        trip_end_date=user_data['trip_end_date'],
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_token(db: Session, token: str):
    return db.query(User).filter(User.session_token == token).first()

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    hashed_input = hashlib.sha256((password + user.salt).encode()).hexdigest()
    if hashed_input == user.password:
        user.session_token = uuid.uuid4().hex
        db.commit()
        db.refresh(user)
        return user
    return None

def logout_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.session_token = None
        db.commit()
        return True
    return False

def update_user(db: Session, user_id: int, updates: dict):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    for field, value in updates.items():
        if hasattr(user, field):
            setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    
    db.delete(user)
    db.commit()


def add_past_destination(db: Session, user_id: int, data: dict):
    destination = PastDestination(
        user_id=user_id,
        destination_name=data["destination_name"],
        trip_start_date=data.get("trip_start_date"),
        trip_end_date=data.get("trip_end_date"),
        rating=data.get("rating"),
        notes=data.get("notes")
    )
    db.add(destination)
    db.commit()
    db.refresh(destination)
    return destination


def get_user_past_destinations(db: Session, user_id: int):
    return db.query(PastDestination).filter(PastDestination.user_id == user_id).all()


def update_past_destination(db: Session, user_id: int, destination_id: int, updates: dict):
    dest = db.query(PastDestination).filter(
        PastDestination.user_id == user_id,
        PastDestination.id == destination_id
    ).first()

    if not dest:
        return {"error": "Past destination not found."}

    for key, value in updates.items():
        if hasattr(dest, key):
            setattr(dest, key, value)

    db.commit()
    db.refresh(dest)
    return dest

def delete_past_destination(db: Session, user_id: int, destination_id: int):
    dest = db.query(PastDestination).filter(
        PastDestination.user_id == user_id,
        PastDestination.id == destination_id
    ).first()

    if not dest:
        return {"error": "Past destination not found."}

    db.delete(dest)
    db.commit()
    return {"message": "Past destination deleted successfully."}

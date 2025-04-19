from sqlalchemy.orm import Session
from recommendation_engine.api.models.destination_models import Destination

def get_destination(db: Session, destination_id: int):
    return db.query(Destination).filter(Destination.id == destination_id).first()


def get_all_destinations(db: Session):
    return db.query(Destination).all()




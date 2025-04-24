from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from recommendation_engine.api.models.database import Base


class PastDestination(Base):
    __tablename__ = "past_destinations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    destination_name = Column(String(255), nullable=False)
    trip_start_date = Column(Date)
    trip_end_date = Column(Date)
    rating = Column(Integer) 
    notes = Column(Text)
    
    
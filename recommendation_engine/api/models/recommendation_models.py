from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from recommendation_engine.api.models.database import Base
from datetime import datetime


class UserRecommendation(Base):
    __tablename__ = "user_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    destination_id = Column(Integer)
    destination_name = Column(Text)
    explanation = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    
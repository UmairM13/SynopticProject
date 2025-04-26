from sqlalchemy import Column, Float, Integer, String
from recommendation_engine.api.models.database import Base

class Destination(Base):
    __tablename__ = 'destinations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    country = Column(String(255))
    off_season_start = Column(String(255))
    off_season_end = Column(String(255))
    avg_daily_budget = Column(Float)
    currency = Column(String(255))
    climate = Column(String(255))
    terrain = Column(String(255))
    holiday_type = Column(String(255))
    language = Column(String(255))
    safety_rating = Column(Integer)
    IATA_code = Column(String(3))
    
    def __init__(self, name, country, off_season_start, off_season_end, avg_daily_budget, currency, climate, terrain, holiday_type, language, safety_rating, IATA_code):
        self.name = name
        self.country = country
        self.off_season_start = off_season_start
        self.off_season_end = off_season_end
        self.avg_daily_budget = avg_daily_budget
        self.currency = currency
        self.climate = climate
        self.terrain = terrain
        self.holiday_type = holiday_type
        self.language = language
        self.safety_rating = safety_rating
        self.IATA_code = IATA_code
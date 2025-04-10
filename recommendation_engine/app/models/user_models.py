from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.sql import func
from models.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nationality = Column(String(100))
    current_city = Column(String(255))
    current_country = Column(String(255))
    age = Column(Integer)
    preferred_climate = Column(String(100))
    preferred_terrain = Column(String(100))
    past_destinations = Column(String)  # TEXT type
    budget = Column(Float)
    holiday_type = Column(String(100))
    trip_start_date = Column(Date)
    trip_end_date = Column(Date)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255))
    salt = Column(String(255))
    session_token = Column(String(255))
    created_at = Column(DateTime, default=func.now())

    def __init__(self, nationality, current_city, current_country, age, 
                 preferred_climate, preferred_terrain, past_destinations, 
                 budget, holiday_type, trip_start_date=None, trip_end_date=None,
                 email=None, password=None, salt=None, session_token=None):
        self.nationality = nationality
        self.current_city = current_city 
        self.current_country = current_country
        self.age = age
        self.preferred_climate = preferred_climate
        self.preferred_terrain = preferred_terrain
        self.past_destinations = past_destinations
        self.budget = budget
        self.holiday_type = holiday_type
        self.trip_start_date = trip_start_date
        self.trip_end_date = trip_end_date
        self.email = email
        self.password = password
        self.salt = salt
        self.session_token = session_token
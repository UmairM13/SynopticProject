from sqlalchemy import Column, Integer, String, Float
from models.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nationality = Column(String(255))
    current_city = Column(String(255))
    current_country = Column(String(255))
    age = Column(Integer)
    preferred_destination = Column(String(255))
    past_destinations = Column(String(255))
    budget = Column(Float)
    holiday_type = Column(String(255))

    def __init__(self, nationality, current_city, current_country, age, preferred_destination, past_destinations, budget, holiday_type):
        self.nationality = nationality
        self.current_city = current_city 
        self.current_country = current_country
        self.age = age
        self.preferred_destination = preferred_destination
        self.past_destinations = past_destinations
        self.budget = budget
        self.holiday_type = holiday_type

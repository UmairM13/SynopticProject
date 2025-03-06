from .database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nationality = db.Column(db.String(255))
    current_city = db.Column(db.String(255))
    current_country = db.Column(db.String(255))
    age = db.Column(db.Integer)
    preferred_destination = db.Column(db.String(255))
    past_destinations = db.Column(db.String(255))
    budget = db.Column(db.Float)
    holiday_type = db.Column(db.String(255))
    
    
    def __init__(self, nationality, current_city, current_country, age, preferred_destination, past_destinations, budget, holiday_type):
        self.nationality = nationality
        self.current_city = current_city 
        self.current_country = current_country
        self.age = age
        self.preferred_destination = preferred_destination
        self.past_destinations = past_destinations
        self.budget = budget
        self.holiday_type = holiday_type
        
    
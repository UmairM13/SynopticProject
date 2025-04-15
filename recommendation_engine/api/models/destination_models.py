from .database import db

class Destination(db.Model):
    __tablename__ = 'destinations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    country = db.Column(db.String(255))
    off_season_start = db.Column(db.String(255))
    off_season_end = db.Column(db.String(255))
    avg_daily_budget = db.Column(db.Float)
    currency = db.Column(db.String(255))
    climate = db.Column(db.String(255))
    terrain = db.Column(db.String(255))
    language = db.Column(db.String(255))
    safety_rating = db.Column(db.Integer)
    
    def __init__(self, name, country, off_season_start, off_season_end, avg_daily_budget, currency, climate, terrain, language, safety_rating):
        self.name = name
        self.country = country
        self.off_season_start = off_season_start
        self.off_season_end = off_season_end
        self.avg_daily_budget = avg_daily_budget
        self.currency = currency
        self.climate = climate
        self.terrain = terrain
        self.language = language
        self.safety_rating = safety_rating
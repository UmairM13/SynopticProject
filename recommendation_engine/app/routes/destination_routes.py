from flask import Blueprint, request, jsonify
from models.database import db
from models.destination_models import Destination

destination_blueprint = Blueprint('destination_routes', __name__)

# Add a new destination
@destination_blueprint.route('/destinations', methods=['POST'])
def add_destination():
    data = request.get_json()
    new_destination = Destination(
        name=data['name'],
        country=data['country'],
        off_season_start=data['off_season_start'],
        off_season_end=data['off_season_end'],
        avg_daily_budget=data['avg_daily_budget'],
        currency=data.get('currency', ""),
        climate=data.get('climate', ""),
        terrain=data.get('terrain', ""),
        language=data.get('language', ""),
        safety_rating=data.get('safety_rating', 0)
    )
    
    db.session.add(new_destination)
    db.session.commit()
    
    return jsonify({"message": "Destination added successfully", "destination_id": new_destination.id}), 201

# Get all destinations
@destination_blueprint.route('/destinations', methods=['GET'])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([{
        "id": destination.id,
        "name": destination.name,
        "country": destination.country,
        "off_season_start": destination.off_season_start,
        "off_season_end": destination.off_season_end,
        "avg_daily_budget": destination.avg_daily_budget,
        "currency": destination.currency,
        "climate": destination.climate,
        "terrain": destination.terrain,
        "language": destination.language,
        "safety_rating": destination.safety_rating
    } for destination in destinations])

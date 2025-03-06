from flask import Blueprint, request, jsonify
from models.database import db
from models.users_models import User

user_blueprint = Blueprint('user_routes', __name__)

@user_blueprint.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
                    nationality=data['nationality'],
                    current_city=data['current_city'],
                    current_country=data['current_country'],
                    age=data['age'],
                    preferred_destination=data['preferred_destination'],
                    past_destinations=data['past_destinations'],
                    budget=data['budget'],
                    holiday_type=data['holiday_type']
                    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User added successfully", "user_id": new_user.id}), 201




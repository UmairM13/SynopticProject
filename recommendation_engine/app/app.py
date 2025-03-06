import os
from flask import Flask
from models.database import db
from routes.user_routes import user_blueprint
from routes.destination_routes import destination_blueprint


app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) 
DB_PATH = os.path.join(BASE_DIR, "../db.sqlite")  

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(destination_blueprint)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
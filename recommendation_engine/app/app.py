import os
from flask import Flask
from models.database import db
from routes.user_routes import user_blueprint
from routes.destination_routes import destination_blueprint
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(destination_blueprint)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
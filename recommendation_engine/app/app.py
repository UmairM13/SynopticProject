from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(destination_blueprint)

if __name__ == '__main__':
    with app.app_context:
        db.create_all()
    app.run()
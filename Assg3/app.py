from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:haslo@localhost:5434/assgdb'

    db.init_app(app)
    migrate = Migrate(app, db)

    from routes import register_routes
    register_routes(app, db)

    with app.app_context():
        try:
            db.create_all()
            db.session.commit()
        except Exception as e:
            print(e)
    return app

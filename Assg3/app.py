from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:haslo@localhost:5432/assgdb'

db = SQLAlchemy()
db.init_app(app)

from routes import register_routes
register_routes(app, db)

with app.app_context():
    try:
        db.create_all()

    except Exception as e:
        print(e)


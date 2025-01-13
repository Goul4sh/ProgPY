from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text

app = Flask(__name__, template_folder='templates')

db = SQLAlchemy()

def create_app():

    engine = create_engine('postgresql://postgres:haslo@localhost:5432/postgres')
    db_name = 'assgdb'
    with engine.connect() as connection:
        result = connection.execute(text(f"Select 1 from pg_database WHERE datname = '{db_name}'"))
        if not result.fetchone():
            connection.execute(text("COMMIT"))
            connection.execute(text(f"CREATE DATABASE {db_name}"))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:haslo@localhost:5432/assgdb'

    db.init_app(app)

    from routes import register_routes
    register_routes(app, db)

    with app.app_context():
        try:
            db.create_all()
            db.session.commit()

        except Exception as e:
            print(e)
    return app

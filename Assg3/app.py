import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

db = SQLAlchemy()


def apply_migrations():
    from flask_migrate import init, migrate, upgrade

    migrations_dir = os.path.join(os.getcwd(), "migrations")
    if not os.path.exists(migrations_dir):
        init()
    migrate(message="Automated migration update")
    upgrade()


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

            load_data_from_file('data/seeds.txt')

            apply_migrations()
        except Exception as e:
            print(e)
    return app


def load_data_from_file(file_path):
    try:
        from models import Seed
        if not Seed.query.first():
            print("Database is empty. Loading data")

            with open(file_path, 'r') as file:
                for line in file:
                    fields = line.strip().split(',')
                    seed = Seed(
                        area=round(float(fields[0]),4),
                        perimeter=round(float(fields[1]),4),
                        compactness=round(float(fields[2]),4),
                        kernel_length=round(float(fields[3]),4),
                        kernel_width=round(float(fields[4]),4),
                        asymmetry_coefficient=round(float(fields[5]),4),
                        kernel_groove_length=round(float(fields[6]),4),
                        seed_class=int(fields[7])
                    )
                    db.session.add(seed)
                db.session.commit()
                print("Data loaded successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Failed to load data: {e}")

from app import db

class Seed(db.Model):
    __tablename__ = 'seeds'

    seed_id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Float, nullable=False)
    perimeter = db.Column(db.Float, nullable=False)
    compactness = db.Column(db.Float, nullable=False)
    kernel_length = db.Column(db.Float, nullable=False)
    kernel_width = db.Column(db.Float, nullable=False)
    asymmetry_coefficient = db.Column(db.Float, nullable=False)
    kernel_groove_length = db.Column(db.Float, nullable=False)
    seed_class = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Seed {}>'.format(self.seed_id)

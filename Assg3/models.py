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

    def to_dict(self):
        return {
            'seed_id': self.seed_id,
            'area': self.area,
            'perimeter': self.perimeter,
            'compactness': self.compactness,
            'kernel_length': self.kernel_length,
            'kernel_width': self.kernel_width,
            'asymmetry_coefficient': self.asymmetry_coefficient,
            'kernel_groove_length': self.kernel_groove_length,
            'seed_class': self.seed_class
        }

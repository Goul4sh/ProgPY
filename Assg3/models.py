from app import db

class Seed(db.Model):
    __tablename__ = 'seeds'

    seedid = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Float, nullable=False)
    perimeter = db.Column(db.Float, nullable=False)
    compactness = db.Column(db.Float, nullable=False)
    kernel_length = db.Column(db.Float, nullable=False)
    kernel_width = db.Column(db.Float, nullable=False)
    assymmetry_coefficient = db.Column(db.Float, nullable=False)
    kernel_groove_length = db.Column(db.Float, nullable=False)

    def __init__(self, area, perimeter, compactness, kernel_length, kernel_width, asymmetry_coefficient,
                 kernel_groove_length):
        self.area = area
        self.perimeter = perimeter
        self.compactness = compactness
        self.kernel_length = kernel_length
        self.kernel_width = kernel_width
        self.asymmetry_coefficient = asymmetry_coefficient
        self.kernel_groove_length = kernel_groove_length

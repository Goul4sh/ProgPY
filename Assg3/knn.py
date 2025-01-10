from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from models import Seed
import numpy as np


def train_knn_model():

    seeds = Seed.query.all()
    if not seeds or len(seeds) < 3:
        return None, None

    X = np.array([[seed.area, seed.perimeter, seed.compactness, seed.kernel_length,
                   seed.kernel_width, seed.asymmetry_coefficient, seed.kernel_groove_length]
                  for seed in seeds])
    y = np.array([seed.seed_class for seed in seeds])

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(X)

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(x_scaled, y)

    return knn, scaler

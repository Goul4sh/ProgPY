from Assg2.Sheep import Sheep
from Assg2.Wolf import Wolf
import random


class Meadow:
    def __init__(self, sheep_count, wolf_count):
        self.animals = []
        self._create_animals(sheep_count, wolf_count)

    def _create_animals(self, sheep_count, wolf_count):
        for _ in range(sheep_count):
            sheep = Sheep(round(random.uniform(-10.0, 10.0), 1), round(random.uniform(-10.0, 10.0), 1))
            self.animals.append(sheep)

        for _ in range(wolf_count):
            wolf = Wolf(0.0, 0.0)
            self.animals.append(wolf)

    def move_animal(self, animal, delta_x, delta_y):

        if isinstance(animal, Sheep):
            delta_x *= 0.5
            delta_y *= 0.5
        elif isinstance(animal, Wolf):
            delta_x *= 1.0
            delta_y *= 1.0

        animal.pos_x += delta_x
        animal.pos_y += delta_y

        animal.pos_x = round(animal.pos_x, 1)
        animal.pos_y = round(animal.pos_y, 1)

    def get_all_positions(self):
        return [(type(animal).__name__, animal.pos_x, animal.pos_y) for animal in self.animals]

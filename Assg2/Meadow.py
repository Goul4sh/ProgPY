from Assg2.Sheep import Sheep
from Assg2.Wolf import Wolf
import random
import math


class Meadow:
    def __init__(self, sheep_count, max_rounds):
        self.sheep = []
        self.max_rounds = max_rounds
        self.rounds = 0
        self._create_sheep(sheep_count)
        self.wolf = Wolf(0.0, 0.0)

    def _create_sheep(self, sheep_count):
        for i in range(1, sheep_count + 1):
            pos_x = random.uniform(-10.0, 10.0)
            pos_y = random.uniform(-10.0, 10.0)
            sheep = Sheep(pos_x, pos_y, i)
            self.sheep.append(sheep)

    def start_simulation(self):
        if self.rounds >= self.max_rounds or len(self.sheep) == 0:
            return False

        self.rounds += 1

        for sheep in self.sheep:
            sheep.move_randomly()

        sheep_to_eat = None
        closest_sheep_distance = float('inf')

        for sheep in self.sheep:
            distance = math.sqrt((self.wolf.pos_x - sheep.pos_x) ** 2 + (self.wolf.pos_y - sheep.pos_y) ** 2)
            real_distance = round(distance, 1)
            if real_distance < closest_sheep_distance:
                closest_sheep_distance = distance
                sheep_to_eat = sheep

        if sheep_to_eat and self.wolf.chase(sheep_to_eat):
            self.sheep.remove(sheep_to_eat)

        return True

    @staticmethod
    def move_animal(animal, delta_x, delta_y):

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

    def get_status(self):
        return {
            "runda": self.rounds,
            "liczba_owiec": len(self.sheep),
            "pozycja_wilka": self.wolf.get_position()
        }

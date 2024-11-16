from Assg2.Animal import Animal
import random


class Sheep(Animal):
    def __init__(self, pos_x, pos_y, sheep_id, move_distance=0.5):
        super().__init__(round(pos_x, 1), round(pos_y, 1))
        self.move_distance = move_distance
        self.sheep_id = sheep_id

    def move_randomly(self):
        direction = random.choice(["north", "south", "east", "west"])
        if direction == "north" and self.pos_x + self.move_distance <= 10:
            self.move(0, self.move_distance)
        elif direction == "south" and self.pos_y - self.move_distance >= -10:
            self.move(0, -self.move_distance)
        elif direction == "east" and self.pos_x + self.move_distance <= 10:
            self.move(self.move_distance, 0)
        elif direction == "west" and self.pos_x - self.move_distance >= -10:
            self.move(-self.move_distance, 0)
        else:
            self.move_randomly()

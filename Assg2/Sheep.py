from Assg2.Animal import Animal
import random


class Sheep(Animal):
    def __init__(self, pos_x, pos_y, sheep_id, move_distance=0.5):
        super().__init__(pos_x, pos_y)
        self.move_distance = move_distance
        self.sheep_id = sheep_id
        self.alive = True

    def get_position_to_json(self):
        if self.alive:
            return {"ID": self.sheep_id, "x": self.pos_x, "y": self.pos_y}
        else:
            return None

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

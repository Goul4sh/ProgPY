import logging

from Animal import Animal
import random


class Sheep(Animal):
    def __init__(self, pos_x, pos_y, sheep_id, move_distance, sheep_pos_limit):
        super().__init__(pos_x, pos_y)
        self.move_distance = move_distance
        self.sheep_id = sheep_id
        self.alive = True
        self.sheep_pos_limit = sheep_pos_limit

    def get_position_to_json(self):
        if self.alive:
            return {"ID": self.sheep_id, "x": self.pos_x, "y": self.pos_y}
        else:
            return None

    def move(self, delta_x, delta_y):
        super().move(delta_x, delta_y)
        logging.debug(f"Sheep {self.sheep_id} moved to position ({self.pos_x: .3f}, {self.pos_y: .3f})")

    def move_randomly(self, attempts=0):
        if attempts >= 10:
            logging.warning(f"Sheep ({self.sheep_id}) failed to move after 10 attempts.")
            return
        direction = random.choice(["north", "south", "east", "west"])
        logging.debug(f"Sheep ({self.sheep_id}) chose {direction}")
        if direction == "north" and self.pos_y + self.move_distance <= self.sheep_pos_limit:
            self.move(0, self.move_distance)
        elif direction == "south" and self.pos_y - self.move_distance >= -self.sheep_pos_limit:
            self.move(0, -self.move_distance)
        elif direction == "east" and self.pos_x + self.move_distance <= self.sheep_pos_limit:
            self.move(self.move_distance, 0)
        elif direction == "west" and self.pos_x - self.move_distance >= -self.sheep_pos_limit:
            self.move(-self.move_distance, 0)
        else:
            self.move_randomly(attempts+1)

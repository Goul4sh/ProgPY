import logging

from Animal import Animal
import math


class Wolf(Animal):
    def __init__(self, pos_x, pos_y, move_distance=1.0):
        super().__init__(pos_x, pos_y)
        self.move_distance = move_distance

    def move(self, delta_x, delta_y):
        super().move(delta_x, delta_y)
        logging.debug(f"Wolf moved to position ({self.pos_x: .3f}, {self.pos_y: .3f})")
        logging.info(f"Wolf moved")

    def chase(self, sheep):
        delta_x = sheep.pos_x - self.pos_x
        delta_y = sheep.pos_y - self.pos_y
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

        print(
            f"Chasing sheep number ({sheep.sheep_id}) on position ({sheep.pos_x: .3f}, "
            f"{sheep.pos_y: .3f}), distance: {distance: .3f}, wolf's range: {self.move_distance}")

        logging.debug(f"Chasing sheep number ({sheep.sheep_id}), distance from sheep: {distance: .3f}")
        logging.info(f"The wolf is chasing the sheep  with number ({sheep.sheep_id})")
        if distance <= self.move_distance:
            self.pos_x = sheep.pos_x
            self.pos_y = sheep.pos_y
            print(f"Sheep number ({sheep.sheep_id}) has been eaten")
            return True
        else:
            move_x = delta_x / distance * self.move_distance
            move_y = delta_y / distance * self.move_distance
            self.move(move_x, move_y)
            return False

    def get_position_to_json(self):
        return {"x": self.pos_x, "y": self.pos_y}

import json
from typing import List


class Animal:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def move(self, delta_x, delta_y):
        self.pos_x += delta_x
        self.pos_y += delta_y

    def get_position(self):
        return self.pos_x, self.pos_y

    def get_position_to_json(self):
        return {
            "position": {
                "x": self.pos_x,
                "y": self.pos_y
            }
        }

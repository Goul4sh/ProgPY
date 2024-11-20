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
        return round(self.pos_x, 1), round(self.pos_y, 1)

    def get_position_to_json(self):
        return {
            "position": {
                "x": self.pos_x,
                "y": self.pos_y
            }
        }

    @staticmethod
    def save_positions(animals: List['Animal'], filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump([animal.get_position_to_json() for animal in animals], file, indent=4)

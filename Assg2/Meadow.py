import csv
import json
import logging
import os

from Sheep import Sheep
from Wolf import Wolf
import random
import math


class Meadow:
    def __init__(self, sheep_count, max_rounds, sheep_pos_limit, sheep_move_dist, wolf_move_dist,
                 filename="pos.json", alive_csv="alive.csv"):
        self.sheep = []
        self.max_rounds = max_rounds
        self.rounds = 0
        self.filename = filename
        self.alive_csv = alive_csv
        self.sheep_pos_limit = sheep_pos_limit
        self.sheep_move_dist = sheep_move_dist
        self.wolf_move_dist = wolf_move_dist
        self.wolf = Wolf(0.0, 0.0, wolf_move_dist)
        self._create_sheep(sheep_count)

        if os.path.exists(self.filename):
            os.remove(self.filename)

        with open(self.alive_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Round', 'Alive sheep'])

    def count_alive_sheep(self):
        return sum(1 for sheep in self.sheep if sheep is not None and sheep.alive)

    def _create_sheep(self, sheep_count):
        for i in range(1, sheep_count + 1):
            pos_x = random.uniform(-self.sheep_pos_limit, self.sheep_pos_limit)
            pos_y = random.uniform(-self.sheep_pos_limit, self.sheep_pos_limit)
            sheep = Sheep(pos_x, pos_y, i, self.sheep_move_dist, self.sheep_pos_limit)
            self.sheep.append(sheep)
            logging.debug(f"Sheep ({sheep.sheep_id}) position ({sheep.pos_x: .3f}, "
                          f"{sheep.pos_y: .3f}) determined")
        logging.info("All sheep positions have been initialized")

    def start_simulation(self):
        if all(sheep is None for sheep in self.sheep):
            logging.info("Simulation ended with all sheep dead")
            return False

        if self.rounds >= self.max_rounds:
            logging.info("Simulation ended with max rounds being achieved")
            return False

        self.rounds += 1

        logging.info(f"round started {self.rounds}")

        for sheep in self.sheep:
            if sheep is not None and sheep.alive:
                sheep.move_randomly()

        sheep_to_eat = None
        closest_sheep_distance = float('inf')

        for sheep in self.sheep:
            if sheep is None:
                continue
            distance = math.sqrt((self.wolf.pos_x - sheep.pos_x) ** 2 + (self.wolf.pos_y - sheep.pos_y) ** 2)
            if distance < closest_sheep_distance:
                closest_sheep_distance = distance
                sheep_to_eat = sheep

        if sheep_to_eat and self.wolf.chase(sheep_to_eat):
            sheep_to_eat.alive = False
            self.sheep[self.sheep.index(sheep_to_eat)] = None
            logging.info(f"Sheep {sheep_to_eat.sheep_id} has been eaten")

        self.save_positions()
        self.save_alive_sheep_count()
        alive_sheep_count = self.count_alive_sheep()
        logging.info(f"Number of alive sheep before the end of round {self.rounds}: {alive_sheep_count}")

        return True

    @staticmethod
    def move_animal(self, animal, delta_x, delta_y):

        if isinstance(animal, Sheep):
            delta_x *= self.sheep_move_dist
            delta_y *= self.sheep_move_dist
        elif isinstance(animal, Wolf):
            delta_x *= self.wolf_move_dist
            delta_y *= self.wolf_move_dist

        animal.pos_x += delta_x
        animal.pos_y += delta_y

    def save_positions(self):
        data = {
            "round_no": self.rounds,
            "sheep_pos": [sheep.get_position_to_json() if sheep is not None else None for sheep in self.sheep],
            "wolf_pos": [self.wolf.get_position_to_json()],
        }

        try:
            with open(self.filename, 'r+', encoding='utf-8') as file:
                lines = file.readlines()
                if lines:
                    file.seek(0, 2)
                    file.write(",\n")
                else:
                    file.write("[\n")

                json.dump(data, file, indent=4)

        except FileNotFoundError:
            with open(self.filename, 'w', encoding='utf-8') as file:
                file.write("[\n")
                json.dump(data, file, indent=4)

        if self.rounds == self.max_rounds or all(sheep is None for sheep in self.sheep):
            with open(self.filename, 'r+', encoding='utf-8') as file:
                lines = file.readlines()
                if lines:
                    lines[-1] = lines[-1].rstrip()
                    lines.append("\n]")
                    file.seek(0)
                    file.writelines(lines)
        logging.debug(f"Saved informations to {self.filename} for round {self.rounds}")

    def save_alive_sheep_count(self):
        alive_sheep = self.count_alive_sheep()
        with open(self.alive_csv, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([f"{self.rounds:<10}", f"{alive_sheep:<10}"])
        logging.debug(f"Saved informations to {self.alive_csv} for round {self.rounds}")

    def get_status(self):
        alive_sheep_count = sum(1 for sheep in self.sheep if sheep is not None and sheep.alive)
        return {
            "round": self.rounds,
            "sheep_count": alive_sheep_count,
            "wolf_position": self.wolf.get_position()
        }

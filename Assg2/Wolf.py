from Assg2.Animal import Animal
import math


class Wolf(Animal):
    def __init__(self, pos_x, pos_y, move_distance=1.0):
        super().__init__(pos_x, pos_y)
        self.move_distance = move_distance

    def chase(self, sheep):
        delta_x = sheep.pos_x - self.pos_x
        delta_y = sheep.pos_y - self.pos_y
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

        print(
            f"Ścigam owcę numer ({sheep.sheep_id}) na pozycji ({round(sheep.pos_x, 1)}, "
            f"{round(sheep.pos_y, 1)}), dystans: {round(distance, 1)}, zasięg wilka: {self.move_distance}")

        if distance <= self.move_distance:
            self.pos_x = sheep.pos_x
            self.pos_y = sheep.pos_y
            print(f"Owca numer ({sheep.sheep_id}) została zjedzona")
            return True
        else:
            move_x = delta_x / distance * self.move_distance
            move_y = delta_y / distance * self.move_distance
            self.move(move_x, move_y)
            return False

    def get_position_to_json(self):
        return {"x": self.pos_x, "y": self.pos_y}

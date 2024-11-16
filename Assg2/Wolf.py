from Assg2.Animal import Animal
import math


class Wolf(Animal):
    def __init__(self, pos_x, pos_y, move_distance=1.0):
        super().__init__(pos_x, pos_y)
        self.move_distance = move_distance

    def chase(self, sheep):
        delta_x = sheep.pos_x - self.pos_x
        x = round(delta_x, 1)
        delta_y = sheep.pos_y - self.pos_y
        y = round(delta_y, 1)
        distance = round(math.sqrt(x ** 2 + y ** 2), 1)

        print(
            f"Ścigam owcę numer ({sheep.sheep_id}) na pozycji ({round(sheep.pos_x, 1)}, "
            f"{round(sheep.pos_y, 1)}), dystans: {distance}, zasięg wilka: {self.move_distance}")

        if distance <= self.move_distance:
            self.pos_x = sheep.pos_x
            self.pos_y = sheep.pos_y
            print(f"Owca numer ({sheep.sheep_id}) została zjedzona")
            return True
        else:
            move_x = delta_x / distance * self.move_distance
            move_y = delta_y / distance * self.move_distance
            changed_pos_x = round(move_x, 1)
            changed_pos_y = round(move_y, 1)
            self.move(changed_pos_x, changed_pos_y)
            return False

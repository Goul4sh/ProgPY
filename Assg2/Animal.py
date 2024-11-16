class Animal:
    def __init__(self, pos_x, pos_y):
        self.pos_x = round(pos_x, 1)
        self.pos_y = round(pos_y, 1)

    def move(self, delta_x, delta_y):
        self.pos_x += round(delta_x, 1)
        self.pos_y += round(delta_y, 1)

    def get_position(self):
        return round(self.pos_x, 1), round(self.pos_y, 1)

class Animal:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_position(self):
        return self.pos_x, self.pos_y

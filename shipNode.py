class ShipNode:
    def __init__(self, coord_length, coord_height):
        self.coord_length = coord_length
        self.coord_height = coord_height
        self.is_not_hit = True

    def on_hit(self):
        self.is_not_hit = False

    def reset(self):
        self.is_not_hit = True

    def is_hit(self):
        return not self.is_not_hit

    def get_coords(self):
        return self.coord_length, self.coord_height
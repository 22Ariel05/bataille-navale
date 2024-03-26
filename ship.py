from shipNode import ShipNode

class Ship:
    def __init__(self, length):
        self.length = length
        self.sunk = False
        self.placed = False
        self.ship_nodes = []

    def get_length(self):
        return self.length

    def is_sunk(self):
        return self.sunk

    def set_sunk(self, sunk_status):
        self.sunk = sunk_status

    def is_placed(self):
        return self.placed

    def set_placed(self, placed_status):
        self.placed = placed_status

    def show_info(self):
        print(f"Ship length: {self.length}, is sunk: {self.sunk}, is placed: {self.placed}")

    def when_placed(self, list_of_coords):
        self.ship_nodes = [ShipNode(coord[0], coord[1]) for coord in list_of_coords]
        self.set_placed(True)

    def on_hit(self, coords_on_hit):
        for node in self.ship_nodes:
            if node.get_coords() == coords_on_hit:
                node.on_hit()
                break
        self.test_is_sunk()

    def test_is_sunk(self):
        if all(node.is_hit() for node in self.ship_nodes):
            self.set_sunk(True)
            return True
        return False
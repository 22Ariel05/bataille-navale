from ship import Ship

class Fleet:
    def __init__(self):
        self.airCarrier = Ship(5)
        self.cruiser = Ship(4)
        self.destroyer1 = Ship(3)
        self.destroyer2 = Ship(3)
        self.submarine1 = Ship(2)
        self.submarine2 = Ship(2)
        self.placed_ships = {}

    def is_ship_available(self, ship_name):
        """Vérifie si un navire n'a pas encore été placé."""
        return ship_name not in self.placed_ships

    def on_hit(self, coords):
        for ship in [self.airCarrier, self.cruiser, self.destroyer1, self.destroyer2, self.submarine1, self.submarine2]:
            if ship.on_hit(coords):
                return True
        return False

    def is_fleet_destroyed(self):
        return all(ship.is_sunk() for ship in [self.airCarrier, self.cruiser, self.destroyer1, self.destroyer2, self.submarine1, self.submarine2])

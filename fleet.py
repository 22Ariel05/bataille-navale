from ship import Ship

class Fleet:
    def __init__(self):
        self.airCarrier = Ship(5)
        self.cruiser = Ship(4)
        self.destroyer1 = Ship(3)
        self.destroyer2 = Ship(3)
        self.submarine1 = Ship(2)
        self.submarine2 = Ship(2)

    def all_ships_placed(self):
        """Vérifie si tous les navires ont été placés."""
        return (
            self.airCarrier.is_placed() and
            self.cruiser.is_placed() and
            self.destroyer1.is_placed() and
            self.destroyer2.is_placed() and
            self.submarine1.is_placed() and
            self.submarine2.is_placed()
        )

    def is_ship_available(self, ship_name):
        """Vérifie si un navire n'a pas encore été placé."""
        ship = getattr(self, ship_name, None)
        return ship and not ship.is_placed()

    def on_hit(self, coords):
        for ship in [self.airCarrier, self.cruiser, self.destroyer1, self.destroyer2, self.submarine1, self.submarine2]:
            if ship.on_hit(coords):
                return True
        return False

    def is_fleet_destroyed(self):
        """Vérifie si toute la flotte est coulée."""
        return all(ship.is_sunk() for ship in [self.airCarrier, self.cruiser, self.destroyer1, self.destroyer2, self.submarine1, self.submarine2])

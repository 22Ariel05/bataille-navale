from ships.ship import Ship

class Cruiser(Ship):
    
    def __init__(self):
        super().__init__(1, 4)

    def showInfo(self):
        print(f"the cruiser is sunk: {self.isSunk}, this cruisers' height is {self.height}, this cruiser is {self.lenght} long, this cruiser is placed: {self.isPlaced}")
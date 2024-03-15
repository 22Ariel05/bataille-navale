from ships.ship import Ship

class Submarine(Ship):
    
    def __init__(self):
        super().__init__(1, 2)

    def showInfo(self):
        print(f"the submarine is sunk: {self.isSunk}, this submarines' height is {self.height}, this submarine is {self.lenght} long, this submarine is placed: {self.isPlaced}")
from ship import Ship

class Destroyer(Ship):
    
    def __init__(self):
        super().__init__(1, 3)

    def showInfo(self):
        print(f"the destroyer is sunk: {self.isSunk}, this destroyers' height is {self.height}, this destroyer is {self.lenght} long, this destroyer is placed: {self.isPlaced}")
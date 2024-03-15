from ship import Ship

class AircraftCarrier(Ship):
    
    def __init__(self):
        super().__init__(1, 5)

    def showInfo(self):
        print(f"the aircraft carrier is sunk: {self.isSunk}, this aircraft carriers' height is {self.height}, this aircraft carrier is {self.lenght} long, this aircraft carrier is placed: {self.isPlaced}")
import numpy as np
from ship import Ship

# playzone can have only 4 kind of value:
#   0 : nothing present
#   1 : boat present
#   2 : miss
#   3 : hit

class Board:
    
    def __init__(self):
        self.playzone = np.zeros(10, 10)      

    def changeBordSituation(self, coordWherelanded):
        if (self.playzone[coordWherelanded[0], coordWherelanded[1]] == 0):
            self.playzone[coordWherelanded[0], coordWherelanded[1]] = 2
        elif (self.playzone[coordWherelanded[0], coordWherelanded[1]] == 1):
            self.playzone[coordWherelanded[0], coordWherelanded[1]] = 3

    def isValdeShot(self, coords):
        if (self.playzone[coords[0], coords[1]] == 0):
            return True
        elif (self.playzone[coords[0], coords[1]] == 1):
            return True
        elif (self.playzone[coords[0], coords[1]] == 2):
            return False
        elif (self.playzone[coords[0], coords[1]] == 3):
            return False
        
    def fitsWherePlayerWants(self, coords, rotate, ship):
        if (rotate):
            if(coords[1] + ship.getLenght - 1 <= 10):
                return True
            else:
                return False
        else:
            if(coords[0] + ship.getLenght - 1 <= 10):
                return True
            else:
                return False
            
    def noOtherShipsPlacedWherePlayerWants(self, coords, rotate, ship):
        if (rotate):
            for i in range(coords[1], coords[1] + ship.getLenght - 1):
                if (self.playzone[coords[0], i] == 1):
                    return False
            return True
        else:
            for i in range(coords[0], coords[0] + ship.getLenght - 1):
                if (self.playzone[i, coords[1]] == 1):
                    return False
            return True

    def isValidPlacement(self, coords, rotate, ship):
        if (self.playzone.noOtherShipsPlacedWherePlayerWants(coords, rotate, ship) or self.playzone.fitsWherePlayerWants(coords, rotate, ship)):
            return True
        else:
            return False

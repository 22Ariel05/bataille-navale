import numpy as np

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



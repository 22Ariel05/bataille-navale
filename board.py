import numpy as np

# playzone can have only 4 kind of value:
#   0 : nothing present
#   1 : boat present
#   2 : miss
#   3 : hit

class Board:
    
    def __init__(self):
        self.playzone = np.zeros(15, 15)
        

def changeBordSituation(self, coordWherelanded):
    if (self.playzone[coordWherelanded[0], coordWherelanded[1]] == 0):
        self.playzone[coordWherelanded[0], coordWherelanded[1]] = 2
    elif (self.playzone[coordWherelanded[0], coordWherelanded[1]] == 1):
        self.playzone[coordWherelanded[0], coordWherelanded[1]] = 3


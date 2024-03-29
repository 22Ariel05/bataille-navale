import numpy as np
from ship import Ship

# playzone can have only 4 kind of value:
#   0 : nothing present
#   1 : boat present
#   2 : miss
#   3 : hit

class Board:
    
    def __init__(self):
        self.playzone = np.zeros((10, 10))      

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
        if rotate:
            # Pour un placement vertical, vérifiez si le navire dépasse le bas de la grille.
            return (coords[0] + ship.get_length() <= 10)
        else:
            # Pour un placement horizontal, vérifiez si le navire dépasse le côté droit de la grille.
            return (coords[1] + ship.get_length() <= 10)

            
    def noOtherShipsPlacedWherePlayerWants(self, coords, rotate, ship):
        length = ship.get_length()
        # Pour un placement vertical
        if rotate:
            # Vérifiez si le placement dépasse le bas de la grille
            if coords[0] + length > 10:
                return False
            for i in range(length):
                # Vérifiez si la position est déjà occupée
                if self.playzone[coords[0] + i][coords[1]] == 1:
                    return False
        # Pour un placement horizontal
        else:
            # Vérifiez si le placement dépasse le côté droit de la grille
            if coords[1] + length > 10:
                return False
            for i in range(length):
                # Vérifiez si la position est déjà occupée
                if self.playzone[coords[0]][coords[1] + i] == 1:
                    return False
        return True


    def isValidPlacement(self, coords, rotate, ship):
        return self.noOtherShipsPlacedWherePlayerWants(coords, rotate, ship) and self.fitsWherePlayerWants(coords, rotate, ship)


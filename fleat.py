import ships.aircraftCarrier as AC
import ships.cruiser as CR
import ships.destroyer as DS
import ships.submarine as SU

class Fleat:
    
    def __init__(self):
        self.airCarry = AC()
        self.cruser = CR()
        self.destroy1 = DS()
        self.destroy2 = DS()
        self.sub1 = SU()
        self.sub2 = SU()

    def isFleatDestroyed(self):
        if (self.airCarry.getIsSunk() and self.cruser.getIsSunk and self.destroy1.getIsSunk and self.destroy2.getIsSunk and self.sub1.getIsSunk and self.sub2.getIsSunk):
            return True
        return False
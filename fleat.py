from ship import Ship

class Fleat:
    
    def __init__(self):
        self.airCarry = Ship(1, 5)
        self.cruser = Ship(1, 4)
        self.destroy1 = Ship(1, 3)
        self.destroy2 = Ship(1, 3)
        self.sub1 = Ship(1, 2)
        self.sub2 = Ship(1, 2)

    def onHit(self):
        if self.airCarry.onHit:
            return
        if self.cruser.onHit:
            return
        if self.destroy1.onHit:
            return
        if self.destroy2.onHit:
            return
        if self.sub1.onHit:
            return
        if self.sub2.onHit:
            return

    def isFleatDestroyed(self):
        if (self.airCarry.getIsSunk() and self.cruser.getIsSunk and self.destroy1.getIsSunk and self.destroy2.getIsSunk and self.sub1.getIsSunk and self.sub2.getIsSunk):
            return True
        return False
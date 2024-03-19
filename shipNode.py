
class ShipNode:

    def __init__(self, coordlenght, coordheight):
        self.coordlenght = coordlenght
        self.coordheight = coordheight
        self.isNotHit = True

    def onHit(self):
        self.isNotHit = False

    def getIsNotHit(self):
        return self.isNotHit
    
    def getCoordlenght(self):
        return self.coordlenght
    
    def getCoordheight(self):
        return self.coordheight
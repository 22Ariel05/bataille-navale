
class ShipNode:

    def __init__(self, coordlenght, coordheight):
        self.lenght = coordlenght
        self.height = coordheight
        self.isNotHit = True

    def onHit(self):
        self.isNotHit = False

    def getIsNotHit(self):
        return self.isNotHit
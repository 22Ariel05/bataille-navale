import numpy as np
from shipNode import ShipNode

class Ship:

    def __init__(self, lenght):
        self.lenght = lenght
        self.isSunk = False
        self.isPlaced = False
        self.shipNode = np.array(dtype=ShipNode)

    def getLenght(self):
        return self.lenght
    
    def getIsSunk(self):
        return self.isSunk
    
    def setIsSunk(self, newIsSunk):
        self.isSunk = newIsSunk

    def getIsPlaced(self):
        return self.isPlaced
    
    def setIsPlaced(self, newIsPlaced):
        self.isPlaced = newIsPlaced

    def showInfo(self):
        print(f"the ship is sunk: {self.isSunk}, this ship is {self.lenght} long, this ship is placed: {self.isPlaced}") 

    def whenPlaced(self, listOfcoords):
        for i in range(len(listOfcoords)):
            np.append(self.shipNode, ShipNode(listOfcoords[i,0], listOfcoords[i,1]))

    def onHit(self, coordsOnHit):
        for shipNode in self.shipNode:
            if shipNode.getCoordlenght() == coordsOnHit[0] and shipNode.getCoordheight() == coordsOnHit[1]: 
                shipNode.onHit()
                
    def testIsSunk(self):
        for shipNode in self.shipNode:
            if shipNode.getIsNotHit():
                return False
        return True
import numpy as np
from shipNode import ShipNode

class Ship:
    def __init__(self, lenght):
        self.lenght = lenght
        self.isSunk = False
        self.isPlaced = False
        # Utiliser une liste vide pour initialiser shipNode
        self.shipNode = []

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
        for coord in listOfcoords:
            # Ici, on suppose que ShipNode prend deux arguments pour les coordonnées
            self.shipNode.append(ShipNode(coord[0], coord[1]))

    def onHit(self, coordsOnHit):
        for shipNode in self.shipNode:
            if shipNode.getCoordlenght() == coordsOnHit[0] and shipNode.getCoordheight() == coordsOnHit[1]: 
                shipNode.onHit()

    def testIsSunk(self):
        for shipNode in self.shipNode:
            if shipNode.getIsNotHit():
                return False
        self.isSunk = True  # Marquer le navire comme coulé si tous les nœuds sont touchés
        return True
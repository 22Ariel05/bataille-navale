class Ship:

    def __init__(self, lenght, height):
        self.lenght = lenght
        self.height = height
        self.isSunk = False
        self.isPlaced = False

    def getLenght(self):
        return self.lenght
    
    def getHeight(self):
        return self.height
    
    def getIsSunk(self):
        return self.isSunk
    
    def setIsSunk(self, newIsSunk):
        self.isSunk = newIsSunk

    def getIsPlaced(self):
        return self.isPlaced
    
    def setIsPlaced(self, newIsPlaced):
        self.isPlaced = newIsPlaced

    def showInfo(self):
        print(f"{self.isSunk} ,{self.height} ,{self.lenght},{self.isPlaced}")   
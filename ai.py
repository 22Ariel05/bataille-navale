import random

class Ai:
    
    def __init__(self):
        self.previousShots = []

    def InitializeAiBoard(self, board, fleet):
        self.placeFleet(board, fleet)

    def placeFleet(self, board, fleet):
        ships = [fleet.airCarry, fleet.cruser, fleet.destroy1, fleet.destroy2, fleet.sub1, fleet.sub2]
        for ship in ships:
            valid_placement = False
            while not valid_placement:
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                rotate = random.choice([True, False])
                if board.isValidPlacement((row, col), rotate, ship):
                    board.placeShip((row, col), rotate, ship)
                    valid_placement = True

    def selectShot(self):
        while True:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if (row, col) not in self.previousShots:
                self.previousShots.append((row, col))
                return [row, col]
            
    # On peut ajouter differentes fonctions pour la difficultée
from board import Board
from fleat import Fleat

class Game:
    
    def __init__(self, isAiOn):
        self.P1Board = Board()
        self.p2Board = Board()

        self.p1Fleat = Fleat()
        self.p2Fleat = Fleat()

        self.isAiOn = isAiOn
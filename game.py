from board import Board
from fleet import Fleat

class Game:
    
    def __init__(self, isAiOn):
        self.P1Board = Board()
        self.p2Board = Board()

        self.p1Fleat = Fleat()
        self.p2Fleat = Fleat()

        self.isAiOn = isAiOn

    def prepFase(self):
        isStillPreping = True
        while (isStillPreping):
            pass

    def combatFase(self):
        while (not self.p1Fleat.isFleatDestroyed() or not self.p2Fleat.isFleatDestroyed()):
            pass


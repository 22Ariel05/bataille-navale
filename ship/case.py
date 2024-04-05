from enum import Enum
from color import Color
import tkinter as tk


class Case(tk.Button):

    def __init__(self, match, x, y):
        super().__init__(match.get_game(), width=5, height=1, padx=0, pady=0)
        self.x = x
        self.y = y
        self.state = CaseState.EMPTY

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state


class CaseState(Enum):
    EMPTY = ("Aucun", Color.WHITE)
    HIT = ("Touché", Color.RED)
    SHIP = ("Navire", Color.GREEN)
    MISS = ("Manqué", Color.BLUE)

    def __init__(self, display_name, color):
        self.display_name = display_name
        self.color = color

    def get_display_name(self):
        return self.display_name

    def get_color(self):
        return self.color